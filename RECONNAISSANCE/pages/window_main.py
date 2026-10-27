
# window.py

from PyQt6.QtWidgets import ( QMainWindow, QWidget, QVBoxLayout,QHBoxLayout, QPushButton, QStackedWidget)
from UI.components import label, panel
from pages.home import HomePage
from pages.recognition import RecognitionPage
from pages.database import DatabasePage
from pages.settings import SettingsPage

class FaceRecognitionUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Reconnaissance faciale")
        self.resize(800, 600)
        self.setMinimumSize(700, 600)

        root = QWidget()
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)

        # En-tête
        header = QHBoxLayout()
        brand = QVBoxLayout()
        brand.addWidget(label("Reconnaissance faciale", "title"))
        brand.addWidget(label("Sécuriser • Identifier", muted=True))
        header.addLayout(brand)
        header.addStretch()

        self.status = label("● Système prêt")
        self.status.setStyleSheet(
            "color:#20D995; font-weight:600;"
        )
        header.addWidget(self.status)
        root_layout.addLayout(header)

        # Corps
        body = QHBoxLayout()
        root_layout.addLayout(body, 1)
        sidebar = panel("sidebar")
        sidebar.setFixedWidth(225)
        side = QVBoxLayout(sidebar)
        side.addWidget(label("MENU PRINCIPAL", muted=True))
        self.stack = QStackedWidget()
        self.nav_buttons = []

        # Création du menu
        for text, index in [
            ("Accueil", 0),
            ("Reconnaissance", 1),
            ("Base de données", 2),
            ("Paramètres", 3),
        ]:
            button = QPushButton(text)
            button.setObjectName("navButton")
            button.setCheckable(True)
            button.clicked.connect(
                lambda checked=False, i=index: self.navigate(i)
            )

            self.nav_buttons.append(button)
            side.addWidget(button)

        side.addStretch()
        side.addWidget(label("Administrateur", muted=True))

        body.addWidget(sidebar)
        body.addWidget(self.stack, 1)

        # Ajout des pages
        self.home_page = HomePage()
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(RecognitionPage(self.navigate))
        self.stack.addWidget(DatabasePage())
        self.stack.addWidget(SettingsPage())
        self.navigate(0)

    def closeEvent(self, event):
        self.home_page.shutdown()
        super().closeEvent(event)

    def navigate(self, index):
        self.stack.setCurrentIndex(index)

        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)
