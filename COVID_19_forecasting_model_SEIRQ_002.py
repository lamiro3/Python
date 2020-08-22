import time
import sys
import numpy as np 
import matplotlib.pylab as plt
from scipy.integrate import odeint
from selenium import webdriver
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

######################################## WebDriver #######################################
options = webdriver.ChromeOptions()
options.add_argument('headless') #크롬 브라우저 백그라운드로 실행
options.add_argument('disable-gpu') #gpu가속 disable

SIRdriver_KOR = webdriver.Chrome(r'COVID_19_forecasting_model\chromedriver.exe', chrome_options = options)
POPdriver_KOR = webdriver.Chrome(r'COVID_19_forecasting_model\chromedriver.exe', chrome_options = options)

SIRdriver_KOR.get('http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun=')
POPdriver_KOR.get('https://superkts.com/population/all')

assert "코로나바이러스감염증-19 > 발생동향 > 국내 발생 현황" in SIRdriver_KOR.title #title이 다음과 다르다면 오류 뜨게끔 함

SIRhtml_KOR = SIRdriver_KOR.page_source
POPhtml_KOR = POPdriver_KOR.page_source

SIRsoup_KOR = BeautifulSoup(SIRhtml_KOR, 'html.parser')
POPsoup_KOR = BeautifulSoup(POPhtml_KOR, 'html.parser')

######################################## GRAPH #######################################
class Graph():
    def SEIRQ(self, x, t, beta, gamma, sigma, alpha, upsilon, q1, q2, q3): 
        
        # t = 시간(일), beta = 감염의 효과율, gamma = 회복률 = 감염지속시간의 역수, sigma = 취약자가 접촉자로 전환될 확률
        # alpha = 질병유발사망률(치사율), upsilon = 접촉자가 감염자로 전환될 확률
        # q1 = 취약자 집단의 검역(격리)률 = 자가격리률 , q2 = 접촉자 집단의 검역(격리)률, q3 = 감염자 집단의 검역(격리)률

        s = x[0] # 전체 취약자수 중 격리자 x
        i = x[1] # 전체 감염자수 중 격리자 x
        r = x[2] # 전체 회복자수
        e = x[3] # 전체 접촉자(의심자=잠복기인사람+비감염자)수 중 격리자 x
        q_s = x[4] # 전체 취약자수 중 격리자 
        q_e = x[5] # 전체 접촉자(의심자=잠복기인사람+비감염자)수 중 격리자 
        q_i = x[6] # 전체 감염자수 중 격리자 

        dsdt = -beta*s*i - sigma*beta*s*e - q1*s # 시간에 따른 전체 취약자수 중 비격리자수 변화율
        didt = upsilon*e - q3*i - alpha*i # 시간에 따른 감염자수 중 비격리자수 변화율
        drdt = gamma*q_i + alpha*i + alpha*q_i# 시간에 따른 회복자수 변화율
        dedt = beta*s*i + sigma*beta*s*e - upsilon*e - q2*e # 시간에 따른 접촉자수 중 비격리자수 변화율
        dq_sdt = q1*s # 시간에 따른 전체 취약자수 중 격리자수 변화율
        dq_edt = q2*e - upsilon*q_e # 시간에 따른 전체 접촉자수 중 격리자수 변화율
        dq_idt = q3*i + upsilon*q_e - gamma*q_i - alpha*q_i # 시간에 따른 전체 감염자수 중 격리자수 변화율

        y = [dsdt, didt, drdt, dedt, dq_sdt, dq_edt, dq_idt]
        return y
    
    def _plot(self, func, x, t, beta, gamma, sigma, alpha, upsilon, q1, q2, q3, N):
        result = odeint(func, x, t, args=(beta, gamma, sigma, alpha, upsilon, q1, q2, q3))
        plt.plot(t, result[:,0]/N*100, 'b', label='Susceptible') #취약자(비격리자) 동향 - 백분율
        plt.plot(t, result[:,1]/N*100, 'r', label='Infective') #감염자(비격리자) 동향 - 백분율
        plt.plot(t, result[:,2]/N*100, 'g', label='Recovered') #회복자 동향 - 백분율
        plt.plot(t, result[:,3]/N*100, 'y', label='Exposed') #접촉자(비격리자) 동향 - 백분율
        plt.plot(t, result[:,4]/N*100, 'c', label='Susceptible_Quarantined') #취약자(격리자) 동향 - 백분율
        plt.plot(t, result[:,5]/N*100, 'm', label='Exposed_Quarantined') #접촉자(격리자) 동향 - 백분율
        plt.plot(t, result[:,6]/N*100, 'k', label='Infective_Quarantined') #감염자(격리자) 동향 - 백분율
        plt.xlabel('days')
        plt.ylabel('number of people (%)')
        plt.title('Republic of Korea')
        plt.legend(loc="upper right")

######################################## Get Data #######################################
class get_KOR_Data():

    confirmed_data_IR = []
    confirmed_data_POP = []

    def __init__(self, confirmed_data_IR, confirmed_data_POP):
        self.confirmed_data_IR = confirmed_data_IR
        self.confirmed_data_POP = confirmed_data_POP

    def getIR(self, soup):
        for pre_data_1 in soup.find_all('table', class_='num minisize'):
            confirmed_data_IR = pre_data_1.find_all('td')
            for i in range(0, len(confirmed_data_IR)):
                confirmed_data_IR[i] = confirmed_data_IR[i].get_text()
        return confirmed_data_IR
    
    def getPOP(self, soup):
        global confirmed_data_POP
        for pre_data_2 in soup.find_all('article', class_='intro'):
            confirmed_data_POP = pre_data_2.find_all('b')
        confirmed_data_POP[0] = confirmed_data_POP[0].get_text()
        #a = confirmed_data_POP[0]
        #confirmed_data_POP[0] = a[:10]
        return confirmed_data_POP
    
    def convertToInt(self, _list):
        for i in range(0, len(_list)):
            _list[i] = _list[i].replace(',','') #천단위 쉼표 제거
            _list[i] = int(_list[i]) #자료형 변환
        return _list

class get_CHN_Data():
    confirmed_data_IR = []
    confirmed_data_POP = []

    def __init__(self, confirmed_data_IR, confirmed_data_POP):
        self.confirmed_data_IR = confirmed_data_IR
        self.confirmed_data_POP = confirmed_data_POP

class get_USA_Data():
    confirmed_data_IR = []
    confirmed_data_POP = []

    def __init__(self, confirmed_data_IR, confirmed_data_POP):
        self.confirmed_data_IR = confirmed_data_IR
        self.confirmed_data_POP = confirmed_data_POP

class get_WORLD_Data():
    confirmed_data_IR = []
    confirmed_data_POP = []

    def __init__(self, confirmed_data_IR, confirmed_data_POP):
        self.confirmed_data_IR = confirmed_data_IR
        self.confirmed_data_POP = confirmed_data_POP

######################################## Print #######################################
class MyWindow(QWidget, Graph):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.fig = plt.figure(figsize=(70,70)) #출력되는 그래프 크기
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

        self.canvas.draw()

        self.setLayout(layout)

        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle("COVID-19 SIR forecasting model")

        self.show()

printGraph = Graph()
GKD = get_KOR_Data(list(), list())

pre_POP_KOR = GKD.convertToInt(GKD.getPOP(POPsoup_KOR)) # 인구
pre_IR_KOR = GKD.convertToInt(GKD.getIR(SIRsoup_KOR)) 
# (순서대로) - [0](확진판정 후)격리중, [1]격리해제, [2]사망, [3][0,1,2]합계, [4](검사)결과음성, [5][3,4]합계, [6]검사중, [7]총합계

# <quit all drivers>
SIRdriver_KOR.quit()
POPdriver_KOR.quit()

# <constant>
covid_19_R0 = 2.25 # 코로나 바이러스 기초감염재생산수(2 - 2.5)
gamma_input = 1/14 # 코로나 바이러스 전염가능시간 = 약 14일 이내 --> 회복률은 전염가능시간의 역수
sigma_input = 1/14 # 취약자가 접촉자로 전환될 확률
self_quarantined = 476267 # 8월 초 기준 국내 자가격리자 수

# <variable - korea>
Population_input_KOR = pre_POP_KOR[0] # 전체 인구
case_negative = pre_IR_KOR[4] # 검사 결과 음성

Dead = pre_IR_KOR[2] # 전체 감염자수 중 사망자수

Susceptible_non_q = Population_input_KOR - self_quarantined - case_negative - pre_IR_KOR[0] - pre_IR_KOR[1] - pre_IR_KOR[2] - pre_IR_KOR[6] # 전체 취약자수 중 비격리자수
Susceptible_q = self_quarantined # 전체 취약자수 중 격리자수(자가격리자 수)
Susceptible = Susceptible_q + Susceptible_non_q # 전체 취약자수

Infective_non_q = 0 # 전체 감염자수 중 비격리자수
Infective_q = pre_IR_KOR[0] # 전체 감염자수 중 격리자수 
Infective = Infective_q + Infective_non_q + Dead # 전체 감염자수

Recovered = pre_IR_KOR[1] # 전체 회복자수((확진 판정 후)격리 해제자 수)

Exposed_non_q = case_negative # 전체 접촉자수 중 비격리자수 
Exposed_q = pre_IR_KOR[6] # 전체 접촉자수 중 격리자수
Exposed = Exposed_q + Exposed_non_q # 전체 접촉자수

alpha_input_KOR = Dead/Infective # 질병유발사망률(치사율)
beta_input_KOR = gamma_input*covid_19_R0/Susceptible # beta = gamma*R0/S
upsilon_input_KOR = Infective/Exposed # 접촉자가 감염자로 전환될 확률

q1_input_KOR = Susceptible_q/Susceptible # 취약자 집단의 검역(격리)률
q2_input_KOR = Exposed_q/Exposed # 접촉자 집단의 검역(격리)률 -- 방역이 완벽하게 일어난다는 가정하에 설정된 값이므로 1 -- 무조건 격리
q3_input_KOR = Infective_q/Infective # 감염자 집단의 검역(격리)률 -- 방역이 완벽하게 일어난다는 가정하에 설정된 값이므로 1 -- 무조건 격리

t_input_KOR = np.linspace(0, 200) #시간 범위 설정(가로축 범위 설정) - 단위: 일(day)
x_input_KOR = [Susceptible_non_q, Infective_non_q, Recovered, Exposed_non_q, Susceptible_q, Exposed_q, Infective_q]

app=QApplication(sys.argv)
w=MyWindow()
printGraph._plot(printGraph.SEIRQ, x_input_KOR, t_input_KOR, beta_input_KOR, gamma_input, sigma_input, alpha_input_KOR, upsilon_input_KOR, q1_input_KOR, q2_input_KOR, q3_input_KOR, Population_input_KOR)
sys.exit(app.exec_()) # exec_()가 루프를 생성하는 함수