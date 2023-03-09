# [2-1]
# income = int(input("본인의 소득을 입력하시오(단위: 10000원): "))

# def Tax(income):
#     if income <= 1200:
#         return 0.06
#     elif income > 1200 and income <= 4600:
#         return 0.15
#     elif income > 4600 and income <= 8800:
#         return 0.24
#     elif income > 8800 and income <= 15000:
#         return 0.35
#     else:
#         return 0.38
    
# print(f'소득 {income*10000}원 기준 근로소득세는 {income*Tax(income)*10000}원 입니다.')
    
# [2-2]
# import random as rd

# answer = rd.randint(0, 99)
# start, end = 0, 99

# for _ in range(10):
#     guess = int(input(f"숫자를 입력하세요(범위: {start}~{end}): "))
    
#     if guess > answer:
#         print("아닙니다. 더 작은 숫자입니다!")
#         end = guess
#     elif guess < answer:
#         print("아닙니다. 더 큰 숫자입니다!")
#         start = guess
#     else:
#         print(f'정답입니다. {_+1}번 만에 맞추셨습니다.')
#         print("게임이 끝났습니다.")
#         break

# [2-3]
# h = int(input("피라미드의 높이를 입력하세요: "))
# GAP = " "
# LEN = 4*h - 3

# for i in range(1, 2*h, 2):
#     side =  GAP*((LEN - i)//2)
#     left, right = str(), str()
    
#     for j in range(1, i, 2):
#         left += (str(j)+GAP)
#         right += (GAP+str(i-1-j))
    
#     print(f'{side}{left}{i}{right}{side}')