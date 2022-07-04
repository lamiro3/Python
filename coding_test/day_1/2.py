remained = int(input())
cnt = 0

def get_coin_num(won):
    global remained
    global cnt
    if remained >= won:
        cnt += remained//won
        remained %= won

while remained != 0:
    get_coin_num(500)
    get_coin_num(100)
    get_coin_num(50)
    get_coin_num(10)

print(cnt)