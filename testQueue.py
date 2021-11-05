from queue import Queue


global m_CspRxQue
m_CspRxQue = Queue()

class tTemp():
    src = None

    def __init__(self):
        pass

def qqqq():
    global m_CspRxQue
    temp = m_CspRxQue.get()
    return temp

if __name__ == "__main__":
    #global m_CspRxQue



    result = tTemp()
    data = bytearray.fromhex('01 02 03 04 05 06 07 08')
    result.src = data

    m_CspRxQue.put(result)

    result1 = tTemp()
    data = bytearray.fromhex('0a 0a 0b 0c 0d 06 07 08')
    result1.src = data

    m_CspRxQue.put(result1)

    temp = qqqq()
    print ("got packet, data=" + ''.join('{:02x} '.format(x) for x in temp.src))

    temp = qqqq()
    print ("got packet, data=" + ''.join('{:02x} '.format(x) for x in temp.src))

    print(f' -----------')
    print(f' -----------')
    print(f' -----------')