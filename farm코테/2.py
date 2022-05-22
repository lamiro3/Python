#문제2
ts = [ t for t in ','.join(input().upper())]
res = ''

def findComma():
  DEL = []
  for i in range(len(ts)-1):
    if ts[i] == ts[i+1] == ',':
      DEL.append(i)  
  
  return DEL

for k in findComma():
  ts.pop(k)

for _ in ts:
  res += _

print(res)