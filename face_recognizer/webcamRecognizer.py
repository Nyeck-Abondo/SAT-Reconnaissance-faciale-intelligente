import cv2 as cv
import face_recognition
import pickle
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage

class WebCamRecongnizer(QThread):
    """
    Classe de détection faciale avec face recognition via la webcam
    """

    def __init__(self, encodings_path="encodings.pickle"):
        super().__init__()
        self.encodingsPath          =   encodings_path;
        self.knowFaceEncoding       =   []
        self.knowFaceName           =   []
        self.running                =   True
        self.loadData()

    def loadData(self):
        """Charge les encodages des visaeges des etudiants"""
        try:
            with open(self.encodingsPath, "rb") as f:
                data = pickle.load(f)
                self.knowFaceEncoding = data["encodings"]
                self.knowFaceName = data["names"]
        except Exception as e :
            print(f"Erreur de chargeent des donnees d'encodage")

    def run(self):
        """
        Boucle de traitement de l'image de la webcam
        """
        capture = cv.VideoCapture(0)

        while self.running:
            ret, frame = capture.read()
            if (not ret):
                continue
            # redimensionnement
            resizedFrame = cv.resize(frame, (0, 0), 0.25, 0.25)
            rgbResizedFrame = cv.cvtColor(resizedFrame, cv.COLOR_BGR2RGB)

            # Detection de visages
            faceLocation = face_recognition.face_locations(rgbResizedFrame)
            faceEncoding = face_recognition.face_encodings(rgbResizedFrame, faceLocation)

            for (top, right, bottom, left), faceEncoding in zip(faceLocation, faceEncoding):
                name = "Inconnue / Unknow"
                confidence = ""

                #comparaison des visages
                compareResult = face_recognition.compare_faces(self.knowFaceEncoding, faceEncoding)
                faceDistance = face_recognition.face_distance(self.knowFaceEncoding, faceEncoding)

                if len(faceDistance) > 0:
                    bestIndex = np.argmin(faceDistance)
                    if compareResult[bestIndex]:
                        name = self.knowFaceName[bestIndex]
                        # score de confiance
                        confidenceValue = (1 - faceDistance[bestIndex])
                        confidence = f"{confidenceValue:.1%}"

                #repositionnement des coordonnees
                top *= 4
                left *= 4
                right *= 4
                bottom *= 4

                #bounding box
                cv.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 3)
                resultText = f"{name} {confidence}".strip()
                cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                font = cv.FONT_HERSHEY_DUPLEX
                cv.putText(frame, resultText, (left + 6, bottom - 6), font, 0.6, (255, 255, 255), 1)