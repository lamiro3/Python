import numpy as np 
import matplotlib.pylab as plt
from scipy.integrate import odeint

plt.ion()
def SIR(x, t, beta, gamma):
    s = x[0] # 전체 취약자수
    i = x[1] # 전체 감염자수
    r = x[2] # 전체 회복자수

    dsdt = -beta*s*i #시간에 따른 취약자수 변화율
    didt = beta*s*i - gamma*i #시간에 따른 감염자수 변화율
    drdt = gamma*i #시간에 따른 회복자수 변화율

    y = [dsdt, didt, drdt]
    return y

def plot_(func, x, t, beta, gamma, N):
    plt.clf()
    result = odeint(func, x, t, args=(beta, gamma))
    plt.plot(t, result[:,0]/N*100, 'b', label='Susceptible') #취약자 동향 - 백분율
    plt.plot(t, result[:,1]/N*100, 'r', label='Infected') #감염자 동향 - 백분율
    plt.plot(t, result[:,2]/N*100, 'g', label='Recovered') #회복자 동향 - 백분율
    plt.xlabel('days(cnt)')
    plt.ylabel('percentage of each population (%)')
    plt.title('Result of simulation')
    plt.legend(loc="upper right")
    plt.show()
    return
