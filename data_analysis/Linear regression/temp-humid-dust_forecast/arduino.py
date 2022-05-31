import serial
import statsmodels.api
import matplotlib.pyplot as plt
import time

def split_data(data):
    output = [0]*3

    arr = data.split(',')
    
    for i in range(3):
        output[i] = float(arr[i])
    
    return output[0], output[1], output[2]

def simple_regression(X, Y):
    X = statsmodels.api.add_constant(X)
    res = statsmodels.api.OLS(Y, X).fit()

    return res

plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False


fig = plt.figure(figsize=(8, 10))
plt.subplots_adjust(hspace= 0.4)

gph1 = fig.add_subplot(3, 1, 1)
gph2 = fig.add_subplot(3, 1, 2)
gph3 = fig.add_subplot(3, 1, 3)

gph1.set_xlabel('시간(초)')
gph2.set_xlabel('시간(초)')
gph3.set_xlabel('시간(초)')

gph1.set_ylabel('습도(%)')
gph2.set_ylabel('온도(oC)')
gph3.set_ylabel('먼지농도(mg/m^3)')


t = [0]*500
temp_c = [0]*500
humid = [0]*500
dust = [0]*500

p_temp_c = [0]*500
p_humid = [0]*500
p_dust = [0]*500

port = 'COM5'
baudrate = 9600

ser = serial.Serial(port, baudrate)

start = time.time()

for k in range(500):
    if ser.readable():

        pd = ser.readline()
        data = pd.decode()[:-2]
    
        now = time.time() - start

        humid[k], temp_c[k], dust[k] = split_data(data)
        t[k] = now

        if k == 0 :
            coef1, coef2, coef3 = 0, 0, 0
            pv1, pv2, pv3 = 0, 0, 0
        
        else:
            coef1 = simple_regression(t[0:k+1], humid[0:k+1]).params[1]
            coef2 = simple_regression(t[0:k+1], temp_c[0:k+1]).params[1]
            coef3 = simple_regression(t[0:k+1], dust[0:k+1]).params[1]

            pv1 = simple_regression(t[0:k+1], humid[0:k+1]).pvalues
            pv2 = simple_regression(t[0:k+1], temp_c[0:k+1]).pvalues
            pv3 = simple_regression(t[0:k+1], dust[0:k+1]).pvalues

        # k+2번째 예측한 값

        if k > 0:
            p_humid[k] = coef1*(t[k] + 10) + simple_regression(t[0:k+1], humid[0:k+1]).params[0]
            p_temp_c[k] = coef2*(t[k] + 10) + simple_regression(t[0:k+1], temp_c[0:k+1]).params[0]
            p_dust[k] =  coef3*(t[k] + 10) + simple_regression(t[0:k+1], dust[0:k+1]).params[0]
        
        else:
            p_humid = humid
            p_temp_c = temp_c
            p_dust = dust
            
        gph1.scatter(t[k], humid[k], color = 'blue', label = '습도')
        gph2.scatter(t[k], temp_c[k], color = 'red', label = '섭씨온도')
        gph3.scatter(t[k], dust[k], color = 'green', label = '먼지농도')

        if k > 0 :
            if (humid[k] >= p_humid[k-1]):
                gph1.vlines(t[k], p_humid[k-1], humid[k], colors = 'black', label = '실측>예측')
                gph1.text(t[k], humid[k], f'{round(humid[k] - p_humid[k-1], 2)}' , color = 'black')
            
            else:
                gph1.vlines(t[k], p_humid[k-1], humid[k], colors = 'yellow', label = '실측<예측')
                gph1.text(t[k], p_humid[k-1], f'{round(humid[k] - p_humid[k-1], 2)}' , color = 'yellow')
        
            if (temp_c[k] >= p_temp_c[k-1]):
                gph2.vlines(t[k], p_temp_c[k-1], temp_c[k], colors = 'black', label = '실측>예측')
                gph2.text(t[k], temp_c[k], f'{round(temp_c[k] - p_temp_c[k-1], 2)}' , color = 'black')
            
            else:
                gph2.vlines(t[k], p_temp_c[k-1], temp_c[k], colors = 'yellow', label = '실측<예측')
                gph2.text(t[k], p_temp_c[k-1], f'{round(temp_c[k] - p_temp_c[k-1], 2)}' , color = 'yellow')
            
            if (dust[k] >= p_dust[k-1]):
                gph3.vlines(t[k], p_dust[k-1], dust[k], colors = 'black', label = '실측>예측')
                gph3.text(t[k], dust[k], f'{round(dust[k] - p_dust[k-1], 2)}' , color = 'black')
            
            else:
                gph3.vlines(t[k], p_dust[k-1], dust[k], colors = 'yellow', label = '실측<예측')
                gph3.text(t[k], p_dust[k-1],  f'{round(dust[k] - p_dust[k-1], 2)}' ,color = 'yellow')

        gph1.scatter(t[k]+10, p_humid[k], color = 'black', alpha = .4, label = '습도_예측값')
        gph2.scatter(t[k]+10, p_temp_c[k], color = 'black', alpha = .4, label = '섭씨온도_예측값')
        gph3.scatter(t[k]+10, p_dust[k], color = 'black', alpha = .4, label = '먼지농도_예측값')

        if k == 0:
            gph1.legend()
            gph2.legend()
            gph3.legend()
        
        #print(pv1, pv2, pv3)
        plt.pause(0.001)

plt.show()