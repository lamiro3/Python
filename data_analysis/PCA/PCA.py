import numpy as np
from math import sqrt
import matplotlib.pyplot as plt

x1 = [-1, 2, 3, 5, 8]
x2 = [10, 7, 5, 1, -3]

mx1, mx2 = np.mean(x1), np.mean(x2) # mean
sd1, sd2 = sqrt(np.var(x1)), sqrt(np.var(x2)) # standard deviation

# mx1, mx2가 0이 되도록 표준화
for i in range(5):
    x1[i] -= mx1
    x1[i] /= sd1
    
    x2[i] -= mx2
    x2[i] /= sd2

X = np.array([x1, x2]).T

# Covariance Matrix
C = X.T.dot(X)

es, ldas = np.linalg.eig(C), np.linalg.eigvals(C)

new_es = [[9.95898769, 0.04101231], [ 0.70710678,  0.70710678]]

changed_X = X.dot(np.array(new_es).T).T

plt.subplot(1, 2, 1)
plt.scatter(x1, x2, c="blue")
plt.hlines(0, -10, 10, colors="black")
plt.vlines(0, -10, 10, colors="black")
for e in new_es:
    plt.arrow(0, 0, e[0], e[1], color="red", head_width = .05, head_length = 0.1)

plt.subplot(1,2,2)
plt.scatter(changed_X[0], changed_X[1], c="blue")
plt.hlines(0, -10, 10, colors="black")
plt.vlines(0, -10, 10, colors="black")

plt.show()