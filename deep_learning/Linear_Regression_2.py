import numpy
import statsmodels.api
from draw_graph import visualize

# TODO transform visualize to matplotlib
def main():
    (N, X, Y) = read_data()
    results = do_simple_regression(N, X, Y)

    visualize(X, Y, results)

def read_data():
    N = int(input().strip())
    X = [0]*N
    Y = [0]*N
    for k in range(N) :
        XY = input().strip().split(" ")
        X[k] = float(XY[0])
        Y[k] = float(XY[1])
    return (N, X, Y)

def do_simple_regression(N, X, Y): #단순회귀분석

    X = numpy.array(X).transpose() #X 전치행렬로 변환
    
    X = statsmodels.api.add_constant(X)
    
    results = statsmodels.api.OLS(Y, X).fit()
    return results

if __name__ == "__main__":
    main()
