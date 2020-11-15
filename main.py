import sys
from random import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np 
import matplotlib.pylab as plt
from scipy.integrate import odeint

class mainScreen(QWidget):
    case_dic = {}
    num = 0
    def __init__(self, case_dic, num):
        super().__init__()
        self.case_dic = case_dic
        self.num = num
        self.initUI()
    
    def initUI(self):
        self.fig = plt.figure(figsize=(70,70)) #출력되는 그래프 크기
        self.canvas = FigureCanvas(self.fig)

        case_label = QLabel("총 인원", self)

        self.case_num = QLineEdit(self)
        self.case_num.textChanged.connect(self.lineEdit_textChanged)

        case_btn = QPushButton("시작", self)
        case_btn.resize(case_btn.sizeHint())
        case_btn.clicked.connect(self.generate_case)

        layout = QHBoxLayout()
        layout.addWidget(case_label)
        layout.addWidget(self.case_num)
        layout.addWidget(case_btn)
        layout.addWidget(self.canvas)

        self.canvas.draw()

        self.setLayout(layout)

        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle("바이러스 확산 시뮬레이션")

        self.show()
    
    def lineEdit_textChanged(self):
        self.num = int(self.case_num.text())

    def generate_case(self):
        for i in range(self.num):
            self.case_dic[f's{i+1}'] = randint(1, self.num)
        print(self.case_dic)

app=QApplication(sys.argv)
w=mainScreen(dict(), int())
sys.exit(app.exec_()) # exec_()가 루프를 생성하는 함수