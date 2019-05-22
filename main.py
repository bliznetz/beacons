import re
testblescan='e1:dc:ab:d3:93:01,0112233445566778899aabbccddeeff0,10011,10003,-59,-51'
first_par = (re.match('^([^,]+)', testblescan)).group()
print(first_par)


topic = first_par.replace(':', '')

print(topic)

r = testblescan.split(',')
v = r[2:6]
print(v)

x=''
for i in v:
    x = x + i + ' '
print(x)




'''
for i in first_par:
    #print(i)
    #print(type(i))
    if i == (re.search(':', first_par)).group(0):
        continue
    else:
        topic = topic + i
        #print(i)
        #print(topic)
print(topic)
'''