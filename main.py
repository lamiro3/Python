import sys
from random import *
from PyQt5.QtWidgets import *
from simulation import *
import numpy as np 
import matplotlib.pylab as plt
from scipy.integrate import odeint

class mainScreen(QWidget):
    case_dic_x = {}
    case_dic_y = {}
    num = 0
    rate = 0
    def __init__(self, case_dic_x, case_dic_y, num, rate):
        super().__init__()
        self.case_dic_x = case_dic_x
        self.case_dic_y = case_dic_y
        self.num = num
        self.rate = rate
        self.initUI()
    
    def initUI(self):
        self.case_label = QLabel("총 인원", self)
        self.socialdis_label = QLabel("사회적 거리두기 비율(0 ~ 100%)", self)

        self.case_num = QLineEdit(self)
        self.case_num.textChanged.connect(self.lineEdit_textChanged_casenum) # 텍스트 입력값 변할 때 함수 실행

        self.socialdis_rate = QLineEdit(self)
        self.socialdis_rate.textChanged.connect(self.lineEdit_textChanged_socialdistancing)

        case_btn = QPushButton("시작", self)
        case_btn.resize(case_btn.sizeHint())
        case_btn.clicked.connect(self.generate_case)

        layout = QHBoxLayout()
        layout.addWidget(self.case_label)
        layout.addWidget(self.case_num)
        layout.addWidget(self.socialdis_label)
        layout.addWidget(self.socialdis_rate)
        layout.addWidget(case_btn)

        self.setLayout(layout)

        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle("바이러스 확산 시뮬레이션")

        self.show()
    
    def lineEdit_textChanged_casenum(self): # 입력한 정수를 int형으로 변환 후 클래스 내의 num 변수에 저장
        self.num = int(self.case_num.text())

    def lineEdit_textChanged_socialdistancing(self):
        self.rate = int(self.socialdis_rate.text())

    def generate_case(self):
        for i in range(self.num):
            self.case_dic_x[f'cx{i+1}'] = randint(-400, 400)
            self.case_dic_y[f'cy{i+1}'] = randint(-400, 400)
            INUM = randint(1, self.num)
        do_simulation(self.case_dic_x, self.case_dic_y, self.num, INUM, self.rate)
        return
        #print(self.case_dic_x)

app=QApplication(sys.argv)
w=mainScreen(dict(), dict(), int(), int())
sys.exit(app.exec_()) # exec_()가 루프를 생성하는 함수