
# pages/settings.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from UI.components import label, panel


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        box = panel()
        content = QVBoxLayout(box)

        content.setContentsMargins(22, 22, 22, 22)
        content.addWidget(label("Paramètres", "title"))
        content.addWidget(label("Apparence : thème sombre"))
        content.addWidget(
            label("Caméra : non connectée", muted=True)
        )
        content.addWidget(
            label("Aucune reconnaissance en cours.", muted=True)
        )
        content.addStretch()

        layout.addWidget(box)
