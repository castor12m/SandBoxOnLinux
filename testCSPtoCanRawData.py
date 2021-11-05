class CSPformat():
    pri         = 0
    src         = 0
    dst         = 0
    dport       = 0
    sport       = 0
    flags       = 0
    userdata    = 0
    len         = 0
    rawdata     = 0


def ShowCSP(csp: CSPformat):
    print(f'\tpri    --- {csp.pri}')
    print(f'\tsrc    --- {csp.src}')
    print(f'\tdst    --- {csp.dst}')
    print(f'\tdport  --- {csp.dport}')
    print(f'\tsport  --- {csp.sport}')
    print(f'\tflags  --- {csp.flags}')
    print('-----------------------------------')

def GenCSPformat(pri:int, src:int, dst:int, dport:int, sport:int, userdata:bytes, flags:int = 0):
    result = CSPformat()

    temp = pri
    if pri > 3:
        temp = 3
    result.pri = temp

    temp = src
    if src > 31:
        temp = 31
    result.src = temp

    temp = dst
    if dst > 31:
        temp = 31
    result.dst = temp

    temp = dport
    if dport > 63:
        temp = 63
    result.dport = temp

    temp = sport
    if sport > 63:
        temp = 63
    result.sport = temp

    temp = flags
    if flags > 255:
        temp = 255
    result.flags = temp

    result.userdata = userdata

    result.len = len(userdata)

    barray = bytearray()

    barr1 = result.pri << 6 | result.src << 1 | ((result.dst & (0b1 << 4)) >> 4)
    barr2 = ((result.dst & 0b1111) << 4) | ((result.dport & (0b1111 << 2)) >> 2)
    barr3 = ((result.dport & 0b11) << 6) | result.sport

    barray.append(barr1)
    barray.append(barr2)
    barray.append(barr3)
    barray.append(result.flags)
    temp = (result.len & (0xFF00)) >> 8
    temp = (result.len & (0x00FF))
    barray.append((result.len & (0xFF00)) >> 8)
    barray.append(result.len & (0xFF))

    for x in result.userdata:
        barray.append(x)

    #barray.append(result.userdata)

    print ("  rawdata [%s]" % (' '.join('{:02x}'.format(x) for x in barray)))

if __name__ == "__main__":
    ''
    
    userdata = 'ab'
    #GenCSPformat(0, 10, 27, 35, 27, userdata.encode(encoding="utf-8"))

    ## testCSPConvert에 코드 합침