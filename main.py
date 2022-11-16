from email import message
from email.mime import image
from re import I, L
import sys
from tkinter import Spinbox
import cv2
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QMainWindow, 
    QHBoxLayout, QVBoxLayout, QPushButton, QFileDialog,
    QSpinBox ,QDoubleSpinBox
)
from PySide6.QtCore import Qt
import numpy as np
import mainFunc


if __name__ == "__main__":
    app = QApplication()
    window = mainFunc.MainFunc()
    window.show()
    sys.exit(app.exec())





