# styles.py

STYLE = """
QMainWindow, QWidget {
    background: #081321;
    color: #E8F0FF;
    font-family: "Segoe UI";
    font-size: 10pt;
}

QFrame#sidebar, QFrame#panel, QFrame#cameraPanel {
    background: #0D1B2D;
    border: 1px solid #1B304A;
    border-radius: 12px;
}

QLabel#title {
    font-size: 20pt;
    font-weight: 700;
}

QLabel#sectionTitle {
    font-size: 12pt;
    font-weight: 600;
}

QLabel#muted {
    color: #91A7C7;
}

QPushButton {
    background: #142943;
    color: #E8F0FF;
    border: 1px solid #213D5C;
    border-radius: 8px;
    padding: 11px 13px;
}

QPushButton:hover {
    background: #1A385B;
}

QPushButton#navButton {
    text-align: left;
    border: none;
    background: transparent;
    padding: 13px;
}

QPushButton#navButton:checked {
    background: #10458A;
}

QPushButton#primary {
    background: #0878F9;
    border-color: #1987FF;
    font-weight: 600;
}

QPushButton#success {
    background: #087D63;
    border-color: #10B981;
    font-weight: 600;
}

QLineEdit {
    background: #081321;
    border: 1px solid #29415F;
    border-radius: 6px;
    padding: 9px;
}

QListWidget, QTableWidget {
    background: #0A1727;
    border: 1px solid #1B304A;
    border-radius: 8px;
    alternate-background-color: #0E2034;
}

QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #1A2C42;
}

QListWidget::item:selected {
    background: #10458A;
}

QHeaderView::section {
    background: #142943;
    color: #DDE9FC;
    padding: 8px;
    border: none;
}

QProgressBar {
    background: #1B304A;
    border: none;
    border-radius: 5px;
    height: 10px;
    text-align: center;
}

QProgressBar::chunk {
    background: #20D995;
    border-radius: 5px;
}
"""