import sys
input = sys.stdin.readline

t = int(input())

def quick_sort(array):
    if len(array) <= 1: return array
    
    pivot, tail = array[0], array[1:]
    
    leftSide = [x for x in tail if x <= pivot]
    rightSide = [x for x in tail if x > pivot]
    
    return quick_sort(leftSide) + [pivot] + quick_sort(rightSide)

def DFS(start, end, k):
    if k == 0:
        results.append(sum(arr[start:end]))
        return
    else:
        
        DFS(start, end-1, k-1)
        DFS(start+2, end, k-1)

for _ in range(t):
    n, k = map(int, input().split())
    arr = quick_sort(list(map(int, input().split())))
    results = []
    DFS(0, n, k)
    print(max(results))