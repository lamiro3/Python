import numpy as np 
import matplotlib.pylab as plt
from scipy.integrate import odeint

plt.ion()

def plot_(x, t, beta, gamma, N, sdrate):
    plt.scatter(t, x[0]/N*100, c = 'b') #취약자 동향 - 백분율
    plt.scatter(t, x[1]/N*100, c = 'r') #감염자 동향 - 백분율
    plt.scatter(t, x[2]/N*100, c = 'g') #회복자 동향 - 백분율
    plt.xlabel('days(cnt)')
    plt.ylabel('percentage of each population (%)')
    plt.title(f'social distancing rate : {sdrate}')
    plt.legend(loc="upper right")
    plt.show()
    return
