
# pages/home.py

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar
)
from PyQt6.QtGui import QPixmap

from UI.components import label, panel
from faceRecognizer.webcamRecognizer import WebCamRecongnizer as wc
from faceRecognizer.face_recognizer import UNKNOWN

class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)

        # Panneau de la caméra
        camera_panel = panel("cameraPanel")
        cam = QVBoxLayout(camera_panel)

        cam.addWidget(
            label("Reconnaissance en temps réel", "sectionTitle")
        )

        self.camera_placeholder = QLabel("PHOTOS / VIDEO")
        self.camera_placeholder.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.camera_placeholder.setMinimumSize(400, 350)

        cam.addWidget(self.camera_placeholder)

        #ajout et initialisatoin du thread de la camera
        self.camera_thread = wc(encodings_path="encodings.pickle")
        # connexions faites UNE seule fois (avant, chaque clic sur "Capturer" en ajoutait une)
        self.camera_thread.image_ready.connect(self.Begin_Capture)
        self.camera_thread.result_ready.connect(self.update_result)


        capture = QPushButton("Capturer")
        capture.setObjectName("primary")
        capture.clicked.connect(self.Capture_Frame)

        reset = QPushButton("Réinitialiser")
        reset.clicked.connect(self.reset_result)

        cam.addWidget(capture)
        cam.addWidget(reset)

        layout.addWidget(camera_panel, 7)

        # Panneau des résultats
        result_panel = panel()
        result = QVBoxLayout(result_panel)

        self.result_banner = label("En attente")
        self.name_value = label("Nom : ")
        self.id_value = label("ID : ")
        self.score_value = label("Niveau de confiance : ")

        result.addWidget(self.result_banner)
        result.addWidget(label("PROFIL IDENTIFIÉ", muted=True))
        result.addWidget(self.name_value)
        result.addWidget(self.score_value)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        result.addWidget(self.progress)

        layout.addWidget(result_panel, 3)

    def Begin_Capture(self, qt_image):
        """ recoit une QImge du thread et l'affiche sur le QLabel"""
        if not self.camera_thread.isRunning():
            return  # image tardive reçue après l'arrêt de la caméra
        self.camera_placeholder.setPixmap(QPixmap.fromImage(qt_image))

    def update_result(self, name, confidence):
        """Affiche le résultat de reconnaissance (visage le plus grand de l'image)"""
        if not name:
            self.result_banner.setText("Aucun visage détecté")
            self.name_value.setText("Nom : —")
            self.score_value.setText("Niveau de confiance : —")
            self.progress.setValue(0)
        elif name == UNKNOWN:
            self.result_banner.setText("Visage inconnu")
            self.name_value.setText("Nom : Inconnu")
            self.score_value.setText("Niveau de confiance : —")
            self.progress.setValue(0)
        else:
            self.result_banner.setText("Visage reconnu")
            self.name_value.setText(f"Nom : {name}")
            self.score_value.setText(f"Niveau de confiance : {confidence:.0f} %")
            self.progress.setValue(int(confidence))

    def Capture_Frame(self, qt_im):
        """Foncton de lancement par le bouton"""
        if not self.camera_thread.isRunning():
            self.camera_thread.start()

    def reset_result(self):
        self.camera_thread.stop()
        self.result_banner.setText("En attente de reconnaissance")
        self.name_value.setText("Nom : ")
        self.score_value.setText("Niveau de confiance : ")
        self.progress.setValue(0)
        self.camera_placeholder.clear()
        self.camera_placeholder.setText("PHOTOS / VIDEO")

    def shutdown(self):
        """Arrête la caméra (appelé à la fermeture de la fenêtre)"""
        if self.camera_thread.isRunning():
            self.camera_thread.stop()
