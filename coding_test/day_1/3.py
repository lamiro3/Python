num = list(input())
isZeroNone = False

if not isZeroNone:
    if '0' in num:
        del num[num.index('0')]
    else:
        isZeroNone = True

result = 1

for n in num:
    result *= int(n)

print(result)