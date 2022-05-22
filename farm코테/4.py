#문제 4
def cal(a, b, i):
  if i == '+':
    return a+b
  elif i == '-':
    return a-b
  elif i == '*':
    return a*b
  else:
    return int(a/b)

def main(): 
    cal_list = input().split(' ')
    print(cal(int(cal_list[0]), int(cal_list[1]), cal_list[2]))

if __name__=="__main__": 
    main()
    