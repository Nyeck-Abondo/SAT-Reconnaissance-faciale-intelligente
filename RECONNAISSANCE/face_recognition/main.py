
# main.py

import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from styles import STYLE
from window_main import FaceRecognitionUI


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLE)

    window = FaceRecognitionUI()
    window.show()

    sys.exit(app.exec())
