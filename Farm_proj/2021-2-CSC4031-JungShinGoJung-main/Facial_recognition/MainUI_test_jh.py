import sys
import threading
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap, QImage
# import RPi.GPIO as GPIO
import time
import datetime

import FaceLogin



class MainWindow(QDialog,QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.Clock()
        self.initUI()
        # self.PirCheck()

    def initUI(self):
        now=datetime.datetime.now()
        hour=now.hour%12
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setStyleSheet("QWidget{background: #000;}")
        self.setAutoFillBackground(True)

        #시간라벨생성
        # Clabel1 = QLabel("%s년 %s월 %s일"%(now.year,now.month,now.day), self)
        # Clabel1.setAlignment(Qt.AlignCenter)
        # Clabel1.setStyleSheet("color: white;")
        # Cfont1 = Clabel1.font()
        # Cfont1.setPointSize(40)
        # Clabel1.setFont(Cfont1)
        #
        # Clabel2 = QLabel("%s시 %s분" %(hour,now.minute),self)
        # Clabel2.setAlignment(Qt.AlignCenter)
        # Clabel2.setStyleSheet("color: white;")
        # Cfont2 = Clabel2.font()
        # Cfont2.setPointSize(40)
        # Clabel2.setFont(Cfont2)
        #
        # layout = QVBoxLayout()
        # layout.addWidget(Clabel1)
        # layout.addWidget(Clabel2)
        # self.setLayout(layout)

    #pir센서로 체크해서 다음으로 넘어가기(쓰레딩필요!!!)
    def PirCheck(self):
        pirPin = 7
        GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)
        counter = 0
        while True:
            if GPIO.input(pirPin) == GPIO.LOW:
                #다음 창 열고, 현재 창 없애는 작업, 초 설정작업 필요
                self.OpenLoginClass()
            else:
                counter += 1

    #다음 윈도우를 열 함수
    def OpenLoginClass(self):
        widget.setCurrentIndex(widget.currentIndex()+1)

    #시간 체크하는 함수 (T쓰레딩 필요!!)
    def Clock(self):
        pass

class PirThread(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        pass


class Login(QDialog):
    def __init__(self) :
        super().__init__()
        self.initUI()
        faceid=FaceLogin.DetectFace()

    def initUI(self):
        pal = QPalette()
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        pal.setColor(QPalette.Background,QColor(0,0,0))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.showFullScreen()


class Medicine(QDialog):
    def __init__(self) :
        super().__init__()


class Emotion(QDialog):
    def __init__(self) :
        super().__init__()


class Exercise(QDialog):
    def __init__(self) :
        super().__init__()





if __name__ == "__main__" :
    app = QApplication(sys.argv)

    # 데스크톱 화면사이즈 구하기
    screen_rect = app.desktop().screenGeometry()
    width, height = screen_rect.width(), screen_rect.height()
    print(width,height)

    #화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()

    #레이아웃 인스턴스 생성
    mainWindow = MainWindow()
    LoginWindow =Login()

    #Widget 추가
    widget.addWidget(mainWindow)
    widget.addWidget(LoginWindow)

    #프로그램 화면을 보여주는 코드
    widget.setFixedHeight(1080)
    widget.setFixedWidth(1920)
    # widget.showFullScreen()
    widget.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
