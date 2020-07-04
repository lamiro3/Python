import numpy as np 
import matplotlib.pylab as plt
from scipy.integrate import odeint

def SIR(x, t, beta, theta, N): # t = 시간(일), beta = 감염의 효과율, theta = 회복률 = 잠복기간의 역수

    s = x[0] # 전체 취약자수
    i = x[1] # 전체 감염자수
    r = x[2] # 전체 회복자수

    dsdt = -beta*s*i #시간에 따른 취약자수 변화율
    didt = beta*s*i - theta*i #시간에 따른 감염자수 변화율
    drdt = theta*i #시간에 따른 회복자수 변화율

    y = [dsdt, didt, drdt]
    return y

covid_19_R0 = 3 #코로나 바이러스 기초감염재생산수 = 2.2 ~ 3.3 이지만 임의로 3으로 지정함

theta_input = 1/5.2 #코로나 바이러스 잠복기간 = 약 5.2일 -- 회복률은 잠복기간의 역수인 1/5.2
Population_input = 48750000 #모집단 인구
beta_input = theta_input*covid_19_R0/(Population_input - 12904) # beta = theta*R0/S
t_input = np.linspace(0, 100) #시간 범위 설정(가로축 범위 설정)
x_input = [Population_input-12984, 1300, 11684] # 차례대로 S, I, R

#print(t_input) --> t값

result = odeint(SIR, x_input, t_input, args=(beta_input, theta_input, Population_input))
# 적분 

plt.figure(figsize=(10,10))
plt.plot(t_input, result[:,0], 'b', label='Susceptible')
plt.plot(t_input, result[:,1], 'r', label='Infected')
plt.plot(t_input, result[:,2], 'g', label='Recovered')
plt.xlabel('days')
plt.ylabel('number of people')
plt.title('Republic of Korea')
plt.legend(loc="upper right")
plt.show()