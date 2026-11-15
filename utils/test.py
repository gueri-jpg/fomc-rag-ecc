import os

a, b = [1], []
s = []
def txt():
    return 1,2
s.append(txt())
print(a)
del a
print(s)
print(s[0])
a = txt()
print(a)
del a