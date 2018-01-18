a = 0b000000000000000000000000000000000000000000000000000101110000110001000000101000000001
print('{:084b}'.format(a))

b = 'WELCOMETOCFF'
d = 0
for i in b:
    c = ord(i)-ord('A')+1
    e = 0b1000000 + c
    #print(d)
    d = (d << 7) + e

print('{:8b}'.format(d))
f = d ^ a
print('{:b}'.format(f))
while f > 0:
    g = f%0b10000000
    #print('{:b}'.format(g))
    f = f>>7
    h = g-0b1000000
    h = h+ord('A')-1
    print(chr(h))


