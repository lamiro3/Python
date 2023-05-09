from collections import deque
import sys

input = sys.stdin.readline

t = int(input())

for _ in range(t):
    
    n, m = map(int, input().split())
    cmds = list(map(int, input().split()))
    cmds.sort(reverse=False)
    seats = deque([0]*m)
    
    for cmd in cmds:
        if cmd == -1:
            lmost = m-1
            for i, seat in enumerate(seats):
                if seat != 0:
                    lmost = i
                    break
                
            if seats[lmost-1] != 0: continue
            else: seats[lmost-1] = 1
        
        elif cmd == -2:
            rmost = 0
            for i, seat in enumerate(seats):
                if seat != 0:
                    rmost = i
                    
            if rmost < m-1:
                if seats[rmost+1] != 0: continue
                else: seats[rmost+1] = 1
                
            elif rmost == m-1:
                if seats[0] != 0: continue
                else: seats[0] = 1
            
        else:
            if seats[cmd-1] == 0:
                seats[cmd-1] = 1

    cnt = 0
    for s in seats:
        if s == 1: cnt+=1
    print(cnt)
                
    