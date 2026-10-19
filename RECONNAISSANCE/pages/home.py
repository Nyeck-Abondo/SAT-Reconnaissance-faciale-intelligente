
# pages/home.py

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar
)
from PyQt6.QtGui import QPixmap

from UI.components import label, panel
from faceRecognizer.webcamRecognizer import WebCamRecongnizer as wc

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
        self.camera_placeholder.setPixmap(QPixmap.fromImage(qt_image))
        self.progress.setValue(0)

    def Capture_Frame(self, qt_im):
        """Foncton de lancement par le bouton"""
        self.camera_thread.image_ready.connect(self.Begin_Capture)
        self.camera_thread.start()

    def reset_result(self):
        self.result_banner.setText("En attente de reconnaissance")
        self.name_value.setText(self.camera_thread.Truename)
        self.score_value.setText("Niveau de confiance : ")
        self.progress.setValue(int(self.camera_thread.Score))
        self.camera_placeholder.setText("PHOTOS / VIDEO")
