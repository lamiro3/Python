#문제 1
def factorial(n):
  if n > 1:
    return n*factorial(n-1)
  else:
    return 1

def main(): 
    n = int(input())
    print(factorial(n))

if __name__=="__main__": 
    main()