import multiprocessing as mp
import os
import pickle
import queue
import time

import cv2 as cv
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage

from faceRecognizer.face_recognizer import UNKNOWN, DEFAULT_TOLERANCE
from faceRecognizer.recognition_worker import recognition_worker

# Racine du projet (dossier qui contient encodings.pickle)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COLOR_KNOWN = (0, 200, 0)       # BGR : vert
COLOR_UNKNOWN = (0, 0, 255)     # BGR : rouge


class WebCamRecongnizer(QThread):
    """
    Détection / reconnaissance faciale via la webcam.

    Pour supprimer la latence, le travail est séparé en deux :
      - ce thread (run) lit la caméra, dessine les cadres et envoie l'image à
        l'interface à la cadence de la caméra : l'affichage n'attend JAMAIS
        la reconnaissance ;
      - un PROCESSUS séparé (recognition_worker) analyse la dernière image
        disponible. Un processus est nécessaire car dlib ne libère pas le GIL :
        dans un simple thread, il figerait quand même l'affichage.
        Une nouvelle image n'est envoyée que lorsque le processus a fini la
        précédente : aucune file d'attente, donc aucun retard qui s'accumule.
    """

    image_ready = pyqtSignal(QImage)
    # (nom, confiance 0-100). nom == "" -> aucun visage ; nom == UNKNOWN -> inconnu
    result_ready = pyqtSignal(str, float)

    DETECT_WIDTH = 320          # largeur de l'image analysée (plus petit = plus rapide)
    UPSAMPLE = 1                # 2 était très coûteux ; 1 suffit pour un visage face à la webcam
    RESULT_TTL = 1.0            # secondes avant d'effacer des cadres devenus obsolètes

    def __init__(self, encodings_path="encodings.pickle",
                 tolerance=DEFAULT_TOLERANCE, camera_index=0):
        super().__init__()
        self.encodingsPath = encodings_path
        self.tolerance = tolerance
        self.cameraIndex = camera_index
        self.knowFaceEncoding = []
        self.knowFaceName = []
        self.running = False
        self.Truename = ""
        self.Score = 0

        self._results = []              # [(top, right, bottom, left, nom, confiance)]
        self._results_time = 0.0
        self._results_version = 0

        self.loadData()

    # ------------------------------------------------------------------ données
    def loadData(self):
        """Charge les encodages des visages des étudiants"""
        path = self.encodingsPath
        if not os.path.isabs(path) and not os.path.isfile(path):
            path = os.path.join(PROJECT_ROOT, path)   # indépendant du dossier de lancement
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)
            self.knowFaceEncoding = [np.asarray(e, dtype=np.float64) for e in data["encodings"]]
            self.knowFaceName = [str(n) for n in data["names"]]
            print(f"[INFO] {len(self.knowFaceEncoding)} encodages chargés depuis {path}")
        except Exception as e:
            self.knowFaceEncoding, self.knowFaceName = [], []
            print(f"[ERREUR] Chargement des données d'encodage impossible ({path}) : {e}")

    # --------------------------------------------------------- boucle caméra
    def _open_camera(self):
        if os.name == "nt":
            capture = cv.VideoCapture(self.cameraIndex, cv.CAP_DSHOW)   # ouverture bien plus rapide sous Windows
        else:
            capture = cv.VideoCapture(self.cameraIndex)
        capture.set(cv.CAP_PROP_BUFFERSIZE, 1)        # pas d'images en retard dans le tampon
        capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
        return capture

    def run(self):
        """Boucle d'affichage : lecture caméra -> cadres -> interface"""
        capture = self._open_camera()
        if not capture.isOpened():
            print("[ERREUR] Impossible d'ouvrir la webcam")
            return

        ctx = mp.get_context("spawn")   # même comportement sous Windows / Linux / macOS
        in_queue, out_queue = ctx.Queue(maxsize=1), ctx.Queue()
        worker = ctx.Process(
            target=recognition_worker, daemon=True,
            args=(in_queue, out_queue, self.knowFaceName, self.knowFaceEncoding,
                  self.tolerance, self.UPSAMPLE))
        worker.start()

        self.running = True
        self._results, self._results_time = [], 0.0
        busy = False                    # le processus est en train d'analyser une image
        last_version = self._results_version

        while self.running:
            ret, frame = capture.read()
            if not ret:
                self.msleep(10)
                continue

            # Récupérer le dernier résultat disponible (sans jamais attendre)
            try:
                while True:
                    self._results = out_queue.get_nowait()
                    self._results_time = time.monotonic()
                    self._results_version += 1
                    busy = False
            except queue.Empty:
                pass

            # Envoyer une image fraîche uniquement si le processus est libre
            if not busy and worker.is_alive():
                scale = self.DETECT_WIDTH / frame.shape[1]
                small = cv.resize(frame, (0, 0), fx=scale, fy=scale)
                in_queue.put((cv.cvtColor(small, cv.COLOR_BGR2RGB), scale))
                busy = True

            results = self._results
            if time.monotonic() - self._results_time > self.RESULT_TTL:
                results = []            # cadres obsolètes (ex. processus encore en démarrage)

            self._draw(frame, results)

            if self._results_version != last_version:
                last_version = self._results_version
                self._publish(results)

            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            height, width, channel = rgb.shape
            # .copy() : le QImage doit posséder ses données (le buffer numpy est réutilisé)
            qt_image = QImage(rgb.data, width, height, channel * width,
                              QImage.Format.Format_RGB888).copy()
            self.image_ready.emit(qt_image)

        # arrêt propre
        try:
            in_queue.put_nowait(None)
        except queue.Full:
            pass
        worker.join(timeout=2)
        if worker.is_alive():
            worker.terminate()
        in_queue.cancel_join_thread()
        out_queue.cancel_join_thread()
        capture.release()

    # ------------------------------------------------------------- utilitaires
    @staticmethod
    def _draw(frame, results):
        font = cv.FONT_HERSHEY_DUPLEX
        for top, right, bottom, left, name, confidence in results:
            known = name != UNKNOWN
            color = COLOR_KNOWN if known else COLOR_UNKNOWN
            text = f"{name} {confidence:.0f}%" if known else UNKNOWN
            cv.rectangle(frame, (left, top), (right, bottom), color, 3)
            cv.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv.FILLED)
            cv.putText(frame, text, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)

    def _publish(self, results):
        """Met à jour Truename / Score et informe l'interface (visage le plus grand)"""
        if results:
            top, right, bottom, left, name, confidence = max(
                results, key=lambda r: (r[2] - r[0]) * (r[1] - r[3]))
            self.Truename = name
            self.Score = int(confidence)
            self.result_ready.emit(name, float(confidence))
        else:
            self.Truename = ""
            self.Score = 0
            self.result_ready.emit("", 0.0)

    def stop(self):
        """Arrête le thread proprement."""
        self.running = False
        self.wait()


# Alias avec l'orthographe correcte
WebCamRecognizer = WebCamRecongnizer
