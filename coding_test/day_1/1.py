N = int(input())
x = [0 for _ in range(N)]
for _ in range(N):
    x[_] = int(input())

print(max(x) - min(x))