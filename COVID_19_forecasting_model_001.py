import time
import numpy as np 
import matplotlib.pylab as plt
from scipy.integrate import odeint
from selenium import webdriver
from bs4 import BeautifulSoup

def SIR(x, t, beta, theta): # t = 시간(일), beta = 감염의 효과율, theta = 회복률 = 잠복기간의 역수

    s = x[0] # 전체 취약자수
    i = x[1] # 전체 감염자수
    r = x[2] # 전체 회복자수

    dsdt = -beta*s*i #시간에 따른 취약자수 변화율
    didt = beta*s*i - theta*i #시간에 따른 감염자수 변화율
    drdt = theta*i #시간에 따른 회복자수 변화율

    y = [dsdt, didt, drdt]
    return y

SIRdriver = webdriver.Chrome('COVID_19_forecasting_model\chromedriver.exe')
POPdriver = webdriver.Chrome('COVID_19_forecasting_model\chromedriver.exe')

SIRdriver.get('http://ncov.mohw.go.kr/')
POPdriver.get('https://superkts.com/population/all')

assert "코로나바이러스감염증-19(COVID-19)" in SIRdriver.title #title이 다음과 다르다면 오류 뜨게끔 함

SIRhtml = SIRdriver.page_source
POPhtml = POPdriver.page_source

SIRsoup = BeautifulSoup(SIRhtml, 'html.parser')
POPsoup = BeautifulSoup(POPhtml, 'html.parser')

class getData(BeautifulSoup):

    confirmed_data_IR = []
    confirmed_data_POP = []

    def __init__(self, confirmed_data_IR, confirmed_data_POP):
        self.confirmed_data_IR = confirmed_data_IR
        self.confirmed_data_POP = confirmed_data_POP

    def getIR(self, soup):
        for pre_data_1 in soup.find_all('ul', class_='liveNum'):
            confirmed_data_IR = pre_data_1.find_all('span', class_='num')
            for i in range(0, len(confirmed_data_IR)):
                confirmed_data_IR[i] = confirmed_data_IR[i].get_text()
        a = confirmed_data_IR[0]
        confirmed_data_IR[0] = a[4:]
        return confirmed_data_IR
    
    def getPOP(self, soup):
        for pre_data_2 in soup.find_all('article', class_='result'):
            confirmed_data_POP = pre_data_2.find_all('h1')
        confirmed_data_POP[0] = confirmed_data_POP[0].get_text()
        a = confirmed_data_POP[0]
        confirmed_data_POP[0] = a[:10]
        return confirmed_data_POP
    
    def convertToInt(self, _list):
        for i in range(0, len(_list)):
            _list[i] = _list[i].replace(',','') #천단위 쉼표 제거
            _list[i] = int(_list[i]) #자료형 변환
        return _list


add = getData(list(), list())

pre_POP = add.convertToInt(add.getPOP(POPsoup)) #인구
pre_IR = add.convertToInt(add.getIR(SIRsoup)) #(순서대로) - [0]누적 확진자수, [1]회복자수, [2]격리자수(치료자수), [3]사망자수

# <quit all drivers>
SIRdriver.quit() 
POPdriver.quit()

# <constant>
covid_19_R0 = 3 #코로나 바이러스 기초감염재생산수 = 2.2 ~ 3.3 이지만 임의로 3으로 지정함
theta_input = 1/5.2 #코로나 바이러스 잠복기간 = 약 5.2일 -- 회복률은 잠복기간의 역수인 1/5.2

# <variable>
Population_input = pre_POP[0] #모집단 인구
beta_input = theta_input*covid_19_R0/(Population_input - pre_IR[0]) # beta = theta*R0/S
t_input = np.linspace(0, 100) #시간 범위 설정(가로축 범위 설정)
x_input = [Population_input - pre_IR[0], pre_IR[2], pre_IR[1]] # 차례대로 S, I, R

#print(t_input) --> t값

result = odeint(SIR, x_input, t_input, args=(beta_input, theta_input))
# 적분 

plt.figure(figsize=(10,10)) #출력되는 그래프 크기
plt.plot(t_input, result[:,0], 'b', label='Susceptible') #취약자 동향
plt.plot(t_input, result[:,1], 'r', label='Infected') #감염자 동향
plt.plot(t_input, result[:,2], 'g', label='Recovered') #회복자 동향
plt.xlabel('days')
plt.ylabel('number of people')
plt.title('Republic of Korea')
plt.legend(loc="upper right")
plt.show()