
# pages/recognition.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from face_recognition.components import label, panel


class RecognitionPage(QWidget):

    def __init__(self, navigate):
        super().__init__()

        layout = QVBoxLayout(self)
        box = panel()
        content = QVBoxLayout(box)

        content.setContentsMargins(22, 22, 22, 22)
        content.addWidget(
            label("Reconnaissance faciale", "title")
        )

        back = QPushButton("Retour à l'accueil")
        back.setObjectName("primary")
        back.clicked.connect(lambda: navigate(0))

        content.addWidget(back)
        content.addStretch()
        layout.addWidget(box)
