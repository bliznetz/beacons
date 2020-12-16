def neg_numbers(x, bits=16):
    mask = (1 << bits) - 1
    #print(abs(x))
    mask = bin(mask)[2:]
    mask = ''.join(mask)
    #print(mask)

    number = bin(x)[2:].zfill(16) #direct form
    print(number)
    y = 0
    s=''
    while 0 <= y <= (len(mask)-1):
        #if int(number[y]) != 0:
            #break
        z = int(mask[y]) & int(number[y])
        #if y == (len(mask) - 1):
        #    z += 1
        y += 1
        s = s + str(z)
    #res = s + bin(x)[2:]
    res = int(s, 2)
    print(s)
    return (res)





print(neg_numbers(0xC5))