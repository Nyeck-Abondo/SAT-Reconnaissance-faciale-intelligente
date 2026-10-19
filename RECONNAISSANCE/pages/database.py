
# pages/database.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)

from UI.components import label, panel


class DatabasePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        box = panel()
        content = QVBoxLayout(box)

        content.addWidget(
            label("Base de données des utilisateurs", "title")
        )

        # Formulaire
        form = QFormLayout()

        self.person_name = QLineEdit()
        self.person_name.setPlaceholderText("Nom complet")

        self.person_id = QLineEdit()
        self.person_id.setPlaceholderText("Identifiant unique")

        self.person_age = QLineEdit()
        self.person_age.setPlaceholderText("Âge (facultatif)")

        form.addRow("Nom complet :", self.person_name)
        form.addRow("Identifiant :", self.person_id)
        form.addRow("Âge :", self.person_age)

        content.addLayout(form)

        save = QPushButton("Enregistrer")
        save.setObjectName("success")
        save.clicked.connect(self.add_person)
        content.addWidget(save)

        # Tableau
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(
            ["Identifiant", "Nom", "Âge"]
        )
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setAlternatingRowColors(True)

        content.addWidget(self.table)
        layout.addWidget(box)

    def add_person(self):
        name = self.person_name.text().strip()
        user_id = self.person_id.text().strip()
        age = self.person_age.text().strip() or "—"

        if not name or not user_id:
            QMessageBox.warning(
                self,
                "Champs obligatoires",
                "Veuillez renseigner le nom et l'identifiant."
            )
            return

        for row in range(self.table.rowCount()):
            existing = self.table.item(row, 0)

            if existing and existing.text() == user_id:
                QMessageBox.warning(
                    self,
                    "Identifiant existant",
                    "Cet identifiant existe déjà."
                )
                return

        row = self.table.rowCount()
        self.table.insertRow(row)

        for col, value in enumerate((user_id, name, age)):
            self.table.setItem(
                row, col, QTableWidgetItem(value)
            )

        self.person_name.clear()
        self.person_id.clear()
        self.person_age.clear()
