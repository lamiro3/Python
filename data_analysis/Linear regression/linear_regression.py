import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import math

T = [333, 363, 373, 383, 393, 403, 413, 423, 433, 443]
sigma = [0.005, 0.00501, 0.005039, 0.005052, 0.005066, 0.005075, 0.005085, 0.005093, 0.005109, 0.005114]

for i in range(len(T)):
  T[i] = T[i]**-1

sigma = list(map(math.log, sigma))

T, sigma = np.array(T).reshape(-1, 1), np.array(sigma).reshape(-1, 1)

# 회귀선 구하기
Model = LinearRegression().fit(T, sigma)

m = Model.coef_[0][0]
n = Model.intercept_[0]

plt.title('graph')
plt.xlabel('1/T')
plt.ylabel('ln(sigma)')
plt.scatter(T, sigma)
plt.plot(T, Model.predict(T), color = 'r')
plt.show()