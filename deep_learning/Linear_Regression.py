import io
import numpy
import statsmodels.api

def main():
    (N, X, Y) = read_data()
    results = do_simple_regression(N, X, Y)
    print(results.summary())

def read_data():
    N = int(input().strip())
    X = [0]*N
    Y = [0]*N
    for k in range(N) :
        XY = input().strip().split(" ")
        X[k] = float(XY[0])
        Y[k] = float(XY[1])
    return (N, X, Y)

def do_simple_regression(N, X, Y):

    X = numpy.array(X).transpose() #X 전치행렬로 변환
    
    X = statsmodels.api.add_constant(X)
    
    results = statsmodels.api.OLS(Y, X).fit()
    return results # 회귀분석 결과 리턴

if __name__ == "__main__":
    main()
