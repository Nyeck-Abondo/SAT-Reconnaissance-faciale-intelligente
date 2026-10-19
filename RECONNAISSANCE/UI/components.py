
# components.py

from PyQt6.QtWidgets import QLabel, QFrame


def label(text, name=None, muted=False):
    widget = QLabel(text)

    if name:
        widget.setObjectName(name)

    if muted:
        widget.setObjectName("muted")

    return widget


def panel(name="panel"):
    widget = QFrame()
    widget.setObjectName(name)
    return widget
