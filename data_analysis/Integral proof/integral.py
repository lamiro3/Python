import matplotlib.pylab as plt
import numpy as np
import sympy as sp
from random import *


fig = plt.figure()

x, y = sp.symbols('x y')
fx = x**2
itg = sp.integrate(fx, (x, 0, 1))

gph1 = fig.add_subplot(2,1,1)
gph2 = fig.add_subplot(2,1,2)

x = np.linspace(0,1, dtype = float)

gph1.plot(x, x**2, 'r')
gph2.plot(x, x**2, 'b--')

gph1.fill_between(x, 0, x**2, where=(x >= 0) & (x <= 1), facecolor='red', alpha=.6)
gph1.text(0.8, .2, f'area = {itg}', fontsize = 12, color='black' ,horizontalalignment='center')

gph1.axhline(0, color='black', alpha=.7)
gph1.axhline(1, color='black', alpha=.7)
gph1.axvline(0, color='black', alpha=.7)
gph1.axvline(1, color='black', alpha=.7)

gph2.axhline(0, color='black', alpha=.7)
gph2.axhline(1, color='black', alpha=.7)
gph2.axvline(0, color='black', alpha=.7)
gph2.axvline(1, color='black', alpha=.7)

cnt1 = 0
cnt2 = 0

for k in range(3000):
    m = random()
    n = random()

    if (n <= m**2):
        gph2.scatter(m, n, color='green', alpha=.7)
        cnt1+=1
    else:
        gph2.scatter(m, n, color='pink', alpha=.7)
        cnt2+=1
    
    if cnt2 != 0 :
        print(float(cnt1/cnt2))

gph2.text(0.8, .2, f'number of dots = {cnt1}', fontsize = 10, color='black' ,horizontalalignment='center')
gph2.text(0.2, .2, f'number of dots = {cnt2}', fontsize = 10, color='black' ,horizontalalignment='center')

plt.show()