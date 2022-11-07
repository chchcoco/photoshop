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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Photoshop")

        # 메뉴바 만들기
        self.menu = self.menuBar()
        self.menu_tool = self.menu.addMenu("파일")
        exit = QAction("나가기", self, triggered=qApp.quit)
        self.menu_tool.addAction(exit)

        save = QAction("수정한 이미지 저장", self, triggered=self.save_img)
        self.menu_tool.addAction(save)


        self.menu_tool = self.menu.addMenu("임계영역/경계검출")
        th_Otsu = QAction("Otsu", self, triggered=self.threshold_Otsu)
        self.menu_tool.addAction(th_Otsu)
        th_adaptM = QAction("Adepted Mean", self, triggered=self.threshold_AdM)
        self.menu_tool.addAction(th_adaptM)
        th_adaptG = QAction("Adepted Gaussian", self, triggered=self.threshold_AdG)
        self.menu_tool.addAction(th_adaptG)
        sh_roberts = QAction("Roverts Corss Filter", self, triggered = self.rovertsCrossFilter)
        self.menu_tool.addAction(sh_roberts)
        sh_sobel = QAction("Sobel Filter", self, triggered = self.sobelFilter)
        self.menu_tool.addAction(sh_sobel)
        

        self.menu_tool = self.menu.addMenu("회전")
        ro_90 = QAction("90도 회전", self, triggered=self.rotate_90)
        self.menu_tool.addAction(ro_90)
        ro_180 = QAction("180도 회전", self, triggered=self.rotate_180)
        self.menu_tool.addAction(ro_180)
        ro_270 = QAction("270도 회전", self, triggered=self.rotate_270)
        self.menu_tool.addAction(ro_270)

        self.menu_tool = self.menu.addMenu("반전")
        flip_x = QAction("상하반전", self, triggered=self.flip_image_x)
        self.menu_tool.addAction(flip_x)
        flip_y = QAction("좌우반전", self, triggered=self.flip_image_y)
        self.menu_tool.addAction(flip_y)
        flip_o = QAction("원점반전", self, triggered=self.flip_image_o)
        self.menu_tool.addAction(flip_o)

        self.menu_tool = self.menu.addMenu("보정")
        normalizing = QAction("노멀라이즈(정규화)", self, triggered=self.normalize_img)
        self.menu_tool.addAction(normalizing)
        equalizing_gray = QAction("이퀄라이즈(흑백)", self, triggered=self.equalize_gray_img)
        self.menu_tool.addAction(equalizing_gray)
        equalizing_color = QAction("이퀄라이즈(컬러))", self, triggered=self.equalize_color_img)
        self.menu_tool.addAction(equalizing_color)
        blur_N= QAction("블러", self, triggered=self.blur_img)
        self.menu_tool.addAction(blur_N)
        blur_G = QAction("가우시안 블러", self, triggered=self.blur_Gaussian)
        self.menu_tool.addAction(blur_G)
        blur_M = QAction("미디언 블러", self, triggered=self.blur_Median)
        self.menu_tool.addAction(blur_M)
        bilateral_Filter = QAction("바이레터널 필터", self, triggered=self.bilateralFiltering_img)
        self.menu_tool.addAction(bilateral_Filter)

        # 메인화면 레이아웃
        main_layout = QHBoxLayout()

        # 사이드바 메뉴버튼
        toolbar = QVBoxLayout()
        button1 = QPushButton("이미지 열기")
        button1.setFixedWidth(120)
        button4 = QPushButton("흑백")
        button4.setFixedWidth(120)
        button6 = QPushButton("확대/축소")
        button6.setFixedWidth(120)
        button7 = QPushButton("알파 블랜드")
        button7.setFixedWidth(120)
        button9 = QPushButton("모시깽")
        button9.setFixedWidth(120)
        button10 = QPushButton("새로고침")
        button10.setFixedWidth(120)

        label1 = QLabel("확대 배율:")
        label1.setAlignment(Qt.AlignLeft)
        label1.setFixedWidth(120)
        label1.setContentsMargins(0,120,0,0)
        self.spinBox1 = QDoubleSpinBox()
        self.spinBox1.setFixedWidth(120)
        self.spinBox1.setMinimum(0.1)
        self.spinBox1.setMaximum(3)
        self.spinBox1.setPrefix("×")
        self.spinBox1.setSingleStep(0.1)
        self.spinBox1_cnt = True
        self.spinBox1.setDisabled(True)

        label2 = QLabel("블랜드 알파값:")
        label2.setAlignment(Qt.AlignLeft)
        label2.setFixedWidth(120)
        label2.setContentsMargins(0,10,0,0)
        self.spinBox2 = QDoubleSpinBox()
        self.spinBox2.setFixedWidth(120)
        self.spinBox2.setMinimum(0.1)
        self.spinBox2.setMaximum(1.0)
        self.spinBox2.setPrefix("α=")
        self.spinBox2.setSingleStep(0.1)
        self.spinBox2_cnt = True
        self.spinBox2.setDisabled(True)

        label3 = QLabel("블러 커널 크기:")
        label3.setAlignment(Qt.AlignLeft)
        label3.setFixedWidth(120)
        label3.setContentsMargins(0,10,0,0)
        self.spinBox3 = QSpinBox()
        self.spinBox3.setFixedWidth(120)
        self.spinBox3.setMinimum(3)
        self.spinBox3.setMaximum(51)
        self.spinBox3.setSingleStep(1)
        self.spinBox3_cnt = True
        self.spinBox3.setDisabled(True)
        self.button11 = QPushButton("블러 적용")
        self.button11.setFixedWidth(120)
        self.button11.setDisabled(True)
        self.blur_cnt=0


        # 버튼 클릭시 함수 작동
        button1.clicked.connect(self.open_img)
        button4.clicked.connect(self.grayScale)
        button6.clicked.connect(self.turn_ExRe)
        button7.clicked.connect(self.turn_blend_Alpha)
        
        button10.clicked.connect(self.clear_label)

        self.spinBox1.valueChanged.connect(self.ex_And_Re)
        self.spinBox2.valueChanged.connect(self.blending_Alpha)
        
        self.spinBox3.valueChanged.connect(self.blur_action)
        self.button11.clicked.connect(self.blur_button)

    # 버튼/위젯 생성
        toolbar.setAlignment(Qt.AlignTop|Qt.AlignLeft)
        toolbar.addWidget(button1)
        toolbar.addWidget(button4)
        toolbar.addWidget(button6)
        toolbar.addWidget(button7)
        toolbar.addWidget(button9)
        toolbar.addWidget(button10)
        
        toolbar.addWidget(label1)
        toolbar.addWidget(self.spinBox1)
        
        toolbar.addWidget(label2)
        toolbar.addWidget(self.spinBox2)
        
        toolbar.addWidget(label3)
        toolbar.addWidget(self.spinBox3)
        toolbar.addWidget(self.button11)


        self.img_label1 = QLabel(self)
        self.img_label1.setFixedSize(720, 640)
        main_layout.addWidget(self.img_label1)


        main_layout.addLayout(toolbar)

    
        self.img_label2 = QLabel(self)
        self.img_label2.setFixedSize(720, 640)
        main_layout.addWidget(self.img_label2)

        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
    
#사진 열기
    def open_img(self):
        file_name = QFileDialog.getOpenFileName(self, "이미지 열기", "./")
        self.image = cv2.imread(file_name[0])
        h, w = self.image.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.image.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label1.setPixmap(pixmap)

#수정된 이미지 저장
    def save_img(self):
        cv2.imwrite("new_image_file.jpg", self.img2)
    

# 반전 y축/x축/원점
    def flip_image_y(self):
        self.img2 = cv2.flip(self.image, 1)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def flip_image_x(self):
        self.img2 = cv2.flip(self.image, 0)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def flip_image_o(self):
        self.img2 = cv2.flip(self.image, -1)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)


 #회전 함수
    def rotate_90(self):
        self.img2 = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def rotate_180(self):
        self.img2 = cv2.rotate(self.image, cv2.ROTATE_180)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def rotate_270(self):
        self.img2 = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

#흑백전환
    def grayScale(self):
        self.img2 = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        h, w = self.img2.shape[:2]
        bytes_per_line =  w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_Grayscale8
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

#임계영역
    def threshold_Otsu(self):
        img= cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, t_otsu = cv2.threshold(img, -1, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
        self.img2=t_otsu
        h, w = self.img2.shape[:2]
        bytes_per_line =  w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_Grayscale8
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def threshold_AdM(self):
        img= cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.img2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 5)
        h, w = self.img2.shape[:2]
        bytes_per_line =  w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_Grayscale8
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)    

    def threshold_AdG(self):
        img= cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.img2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 9, 5)
        h, w = self.img2.shape[:2]
        bytes_per_line =  w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_Grayscale8
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

#노멀라이즈/이퀄라이즈
    def normalize_img(self):
        self.img2 = cv2.normalize(self.image, None, 0, 255, cv2.NORM_MINMAX)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def equalize_gray_img(self):
        self.img2 = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.img2 = cv2.equalizeHist(self.img2)
        h, w = self.img2.shape[:2]
        bytes_per_line =  w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_Grayscale8
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def equalize_color_img(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2YUV)
        img[:,:,0] = cv2.equalizeHist(img[:,:,0])
        self.img2 = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

#확대축소/활성화
    def turn_ExRe(self):
        if self.spinBox1_cnt == True:
            self.spinBox1_cnt = False
            self.spinBox1.setEnabled(True)
        else:
            self.spinBox1_cnt = True
            self.spinBox1.setDisabled(True)

    def ex_And_Re(self, i):
        h, w = self.image.shape[:2]
        self.img2 = cv2.resize(self.image, (int(w*i), int(h*i)), None, 0, 0, cv2.INTER_AREA)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

#알파 블랜드/활성화
    def turn_blend_Alpha(self):
        if self.spinBox2_cnt == True:
            self.spinBox2_cnt = False
            file_name = QFileDialog.getOpenFileName(self, "이미지 열기", "./")
            self.blend_img = cv2.imread(file_name[0])
            self.spinBox2.setEnabled(True)
            h, w = self.image.shape[:2]
            self.blend_img = cv2.resize(self.blend_img, (w, h), None, 0, 0, cv2.INTER_AREA) 
        else:
            self.spinBox2_cnt = True
            self.blend_img = None
            self.spinBox2.setDisabled(True)

    def blending_Alpha(self, i):
        self.img2 = cv2.addWeighted(self.image, i, self.blend_img, (1-i), 0)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)
    
#블러
    def blur_img(self, i=3):
        self.blur_cnt = 1
        self.spinBox3.setSingleStep(1)
        if self.spinBox3_cnt == True:
            self.spinBox3_cnt = False
            self.spinBox3.setEnabled(True)
            self.button11.setEnabled(True)
        self.img2 = cv2.blur(self.image, (i,i))
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def blur_Gaussian(self,i=3):
        self.blur_cnt = 2
        self.spinBox3.setSingleStep(2)
        if self.spinBox3_cnt == True:
            self.spinBox3_cnt = False
            self.spinBox3.setEnabled(True)
            self.button11.setEnabled(True)
        self.img2 = cv2.GaussianBlur(self.image, (i,i), 0)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def blur_Median(self,i=3):       
        self.blur_cnt = 3
        self.spinBox3.setSingleStep(2)
        if self.spinBox3_cnt == True:
            self.spinBox3_cnt = False
            self.spinBox3.setEnabled(True)
            self.button11.setEnabled(True)
        self.img2 = cv2.medianBlur(self.image, i)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def bilateralFiltering_img(self,i=3):       
        self.blur_cnt = 4
        if self.spinBox3_cnt == True:
            self.spinBox3_cnt = False
            self.spinBox3.setEnabled(True)
            self.button11.setEnabled(True)
        self.img2 = cv2.bilateralFilter(self.image, i, 75, 75)
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def blur_action(self, i):
        if self.blur_cnt == 1:
            self.img2 = cv2.blur(self.image, (i,i))
            h, w = self.img2.shape[:2]
            bytes_per_line = 3 * w
            image = QImage(
                self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
            ).rgbSwapped()
            pixmap = QPixmap(image)
            self.img_label2.setPixmap(pixmap)
        elif self.blur_cnt == 2:
            self.img2 = cv2.GaussianBlur(self.image, (i,i), 0)
            h, w = self.img2.shape[:2]
            bytes_per_line = 3 * w
            image = QImage(
                self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
            ).rgbSwapped()
            pixmap = QPixmap(image)
            self.img_label2.setPixmap(pixmap)
        elif self.blur_cnt == 3:
            self.img2 = cv2.medianBlur(self.image, i)
            h, w = self.img2.shape[:2]
            bytes_per_line = 3 * w
            image = QImage(
                self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
            ).rgbSwapped()
            pixmap = QPixmap(image)
            self.img_label2.setPixmap(pixmap)
        elif self.blur_cnt == 4:
            self.img2 = cv2.bilateralFilter(self.image, i, 75, 75)
            h, w = self.img2.shape[:2]
            bytes_per_line = 3 * w
            image = QImage(
                self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
            ).rgbSwapped()
            pixmap = QPixmap(image)
            self.img_label2.setPixmap(pixmap)
        else:
            self.blur_button

    def blur_button(self):   
        self.blur_cnt = 0
        self.spinBox3_cnt = True
        self.spinBox3.setDisabled(True)
        self.button11.setDisabled(True)
        
    def rovertsCrossFilter(self):
        gx = np.array([[1, 0], [0, -1]])
        gy = np.array([[0, 1], [-1, 0]])
        edge_gx = cv2.filter2D(self.image, -1, gx)
        edge_gy = cv2.filter2D(self.image, -1, gy)
        self.img2 = edge_gx + edge_gy
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)

    def sobelFilter(self):
        gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        edge_gx = cv2.filter2D(self.image, -1, gx)
        edge_gy = cv2.filter2D(self.image, -1, gy)
        self.img2 = edge_gx + edge_gy
        h, w = self.img2.shape[:2]
        bytes_per_line = 3 * w
        image = QImage(
            self.img2.data, w, h, bytes_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        pixmap = QPixmap(image)
        self.img_label2.setPixmap(pixmap)


    def clear_label(self):
        self.img_label2.clear()
        self.img2=self.image





if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())





