# CSP CAN Filter 값 할당 분석 용

from typing import SupportsComplex

class CFPformat():
    src         = 0
    dst         = 0
    type        = 0
    remain      = 0
    identifier  = 0

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

def AnalysisCFPData(bytes):
    cfp = CFPformat()

    cfp.src = bytes[0] & 0b11111
    cfp.dst = (bytes[1] & (0b11111 << 3)) >> 3
    cfp.type = (bytes[1] & (0b1 << 2)) >> 2
    cfp.remain = ((bytes[1] & 0b11) << 6) + ((bytes[2] & (0b111111 << 2)) >> 2)
    cfp.identifier = ((bytes[2] & 0b11) << 8) + bytes[3]

    return cfp

def AnalysisCSPData(bytes):
    csp = CSPformat()

    csp.pri = (bytes[0] & (0b11 << 6)) >> 6
    csp.src = (bytes[0] & (0b11111 << 1)) >> 1
    csp.dst = ((bytes[0] & 0b1) << 4) + ((bytes[1] & (0b1111 << 4)) >> 4)
    csp.dport = ((bytes[1] & 0b1111) << 2) + ((bytes[2] & (0b11 << 6)) >> 6)
    csp.sport = bytes[2] & 0b111111
    csp.flags = bytes[3]

    return csp

def GenCFPformat(src:int, dst:int, type:int, remain:int, identifier:int):
    result = CFPformat()

    temp = src
    if src > 31:
        temp = 31
    result.src = temp

    temp = dst
    if dst > 31:
        temp = 31
    result.dst = temp

    temp = type
    if type > 1:
        temp = 1
    result.type = temp

    temp = remain
    if remain > 255:
        temp = 255
    result.remain = temp

    temp = identifier
    if identifier > 1023:
        temp = 1023
    result.identifier = temp

    barray = bytearray()

    barr1 = result.src
    barr2 = (result.dst << 3) |  (result.type << 2) | ((result.remain & (0b11 << 6)) >> 6)
    barr3 = ((result.remain & 0b111111) << 2) | ((result.identifier & (0b11 << 8)) >> 8)
    barr4 = result.identifier

    barray.append(barr1)
    barray.append(barr2)
    barray.append(barr3)
    barray.append(barr4)

    print ("  rawdata [%s]" % (' '.join('{:02x}'.format(x) for x in barray)))

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

def ShowCFP(cfp: CFPformat):
    # print(f'\tsrc --- {cfp.src}')
    # print(f'\tdst --- {cfp.dst}')
    # print(f'\ttyp --- {cfp.type}')
    # print(f'\trem --- {cfp.remain}')
    # print(f'\tid  --- {cfp.identifier}')

    print(f' --- \t src\t, dst\t, type\t, rem\t, id')
    print(f' --- \t {cfp.src}\t, {cfp.dst}\t, {cfp.type}\t, {cfp.remain}\t, {cfp.identifier}')
    print('-----------------------------------')

def ShowCSP(csp: CSPformat):
    # print(f'\tpri    --- {csp.pri}')
    # print(f'\tsrc    --- {csp.src}')
    # print(f'\tdst    --- {csp.dst}')
    # print(f'\tdport  --- {csp.dport}')
    # print(f'\tsport  --- {csp.sport}')
    # print(f'\tflags  --- {csp.flags}')

    print(f' --- \t pri\t, src\t, dst\t, dstP\t, srcP\t, flags')
    print(f' --- \t {csp.pri}\t, {csp.src}\t, {csp.dst}\t, {csp.dport}\t, {csp.sport}\t, {csp.flags}')
    print('-----------------------------------')



if __name__ == "__main__":
    ''
    #2021-10-18 cangaroo -> 10, 1B500000# 36 A2 A9 00 00 02 00 00

    # temp = AnalysisCFPData([0x0A, 0xD8, 0x00, 0x00])
    # ShowCFP(temp)

    # temp = AnalysisCFPData([0x1B, 0x50, 0x00, 0x00])
    # ShowCFP(temp)
    
    # PI --> Other(27)
    # temp = AnalysisCSPData([0x15, 0xB2, 0xA0, 0x00])
    # ShowCSP(temp)

    # PI <-- Other(27)
    # temp = AnalysisCSPData([0x36, 0xA6, 0xCA, 0x00])
    # ShowCSP(temp)

    # pi --> other
    # print('ping target dst: 27 ----------------')
    # temp = AnalysisCFPData([0x1B, 0x58, 0x04, 0x01])
    # ShowCFP(temp)
    # temp = AnalysisCSPData([0x36, 0xB0, 0x4F, 0x00])
    # ShowCSP(temp)

    print(' pi -> sv -------')
    temp = AnalysisCFPData([0x0A, 0xD8, 0x08, 0x00])
    ShowCFP(temp)
    temp = AnalysisCSPData([0x15, 0xB2, 0x80, 0x00])
    ShowCSP(temp)

    print(' pi <- sv -------')
    temp = AnalysisCFPData([0x1B, 0x58, 0x00, 0x01])
    ShowCFP(temp)
    temp = AnalysisCSPData([0x36, 0xB2, 0x8f, 0x00])
    ShowCSP(temp)
    print(' -------------------- ')

    __temp = False
    if __temp:
        userdata = 'ab'
        __src = 10
        __dst = 27
        __dport = 24
        __sport = 38    # 계속 바꿔야 수신측에서 수신 됨...
        GenCFPformat(__src, __dst, 0, 0, 0)
        GenCSPformat(0, __src, __dst, __dport, __sport, userdata.encode(encoding="utf-8"))
        ## canSim -> pv(27) : dport 0 24 // 25부터 안됨 25, 26 27 29 30 40 < 안되는거 확인

    __temp = True
    if __temp:
        userdata = 'ab'
        __src = 27
        __dst = 10
        __dport = 24    # dst 랑 dport랑 맞춰야하나..?
        __sport = 35    # 계속 바꿔야 수신측에서 수신 됨...
        GenCFPformat(__src, __dst, 0, 1, 0)
        GenCSPformat(0, __src, __dst, __dport, __sport, userdata.encode(encoding="utf-8"))

        # canSim -> pi(11) : 1B580000 36 b2 a0 00 00 02 61 62  dport 0 ~ 10 ~ 24 // 25부터 안됨
