import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Importez la classe que nous avons créée précédemment
# Assurez-vous que le nom du fichier correspond (ici on suppose webcam_module.py)
from faceRecognizer.webcamRecognizer import WebCamRecongnizer

class FenetreTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Module Webcam - Reconnaissance Faciale")
        self.resize(800, 600)

        # Widget central et layout
        widget_central = QWidget()
        layout = QVBoxLayout(widget_central)
        self.setCentralWidget(widget_central)

        # Label qui servira d'écran pour la vidéo
        self.label_video = QLabel("Chargement de la webcam...")
        self.label_video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_video)

        # Initialisation du thread de webcam
        # Remplacez "encodings.pickle" par le chemin réel de votre fichier d'encodages
        self.thread_webcam = WebCamRecongnizer(encodings_path="encodings.pickle")
        
        # Connexion du signal à la méthode d'affichage
        self.thread_webcam.image_ready.connect(self.mettre_a_jour_image)
        
        # Démarrage du thread
        self.thread_webcam.start()

    def mettre_a_jour_image(self, qt_image):
        """Reçoit le QImage du thread et l'affiche sur le QLabel."""
        self.label_video.setPixmap(QPixmap.fromImage(qt_image))

    def closeEvent(self, event):
        """Assure l'arrêt propre du flux vidéo et du thread à la fermeture de la fenêtre."""
        self.thread_webcam.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenetreTest()
    fenetre.show()
    sys.exit(app.exec())