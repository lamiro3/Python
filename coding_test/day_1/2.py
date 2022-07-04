N, M = map(int, input().split())
MINS = []

for _ in range(N):
    row = list(map(int, input().split()))
    MINS.append(min(row))

print(max(MINS))