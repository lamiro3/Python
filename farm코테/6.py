#문제 6
prior = {'+':1, '-':1, 'x':2, '/':2}
Input = input()
e_list = []
prev = 0
stack=[]
Output = []

for t in range(len(Input)):
  if not Input[t].isdigit():
    e_list.append(Input[prev:t])
    e_list.append(Input[t])
    prev = t+1
e_list.append(Input[prev:])

def Calculation(ts):
  _stack = []
  for t in ts:
    if t == '+':
      a = _stack.pop()
      b = _stack.pop()
      _stack.append(b+a)
    elif t == '-':
      a = _stack.pop()
      b = _stack.pop()
      _stack.append(b-a)
    elif t == 'x':
      a = _stack.pop()
      b = _stack.pop()
      _stack.append(b*a)
    elif t == '/':
      a = _stack.pop()
      b = _stack.pop()
      _stack.append(b/a)
    else:
      _stack.append(float(t))
  return _stack.pop()
    

for i in e_list:
  if i.isdigit():
    Output.append(i)
  elif not stack:
    stack.append(i)
  else:
    while True:
      if stack and prior[stack[-1]] >= prior[i] :
        Output.append(stack.pop())
      else:
        break
    stack.append(i)

while stack:
  Output.append(stack.pop())

sen = ''

for _ in Output:
  sen += _
print(int(Calculation(Output)))
