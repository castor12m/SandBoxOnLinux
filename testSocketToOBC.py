import socket

class MiniCmdUtil:
    ## Class objects
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self,
                 host="127.0.0.1",
                 port=1234,
                 endian="BE",
                 pktID="0",
                 cmdCode=0,
                 parameters=None,
                 userdata:bytes=None):

        self.host = host
        self.port = int(port)
        self.endian = "big" if endian == "BE" else "little"
        self.pktID = int(pktID, 16)
        self.cmdCode = int(cmdCode)
        self.parameters = parameters

        #self.payload = bytearray()
        #1C 00 C0 00 00 81 00 97
        #udata = '35 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
        #udataBytes = bytearray.fromhex(udata)
        self.payload = userdata

        self.packet = bytearray()

        self.cmdOffsetPri = 0
        self.cmdOffsetSec = 0
        self.checksum = 0xFF
        self.cfsCmdSecHdr = bytearray(2)
        

    def assemblePriHeader(self):
        ccsdsPri = bytearray(6)
        ccsdsPri[:2] = self.pktID.to_bytes(2, byteorder='big')
        ccsdsPri[2:4] = (0xC000).to_bytes(2, byteorder='big')
        totalPacketLen = len(ccsdsPri) + len(self.cfsCmdSecHdr)
        self.assemblePayload()
        totalPacketLen += len(self.payload)
        totalPacketLen += self.cmdOffsetPri + self.cmdOffsetSec
        ccsdsPri[4:] = (totalPacketLen - 7).to_bytes(2, byteorder="big")
        return ccsdsPri

    def assemblePayload(self):
        if self.parameters:
            paramList = self.parameters.split(" ")
            for param in paramList:
                items = param.split("=")  ## e.g. ["--uint16", "2"]
                if "--string" not in param:  ## non-string param
                    dataType = items[0].strip("-")  ## Remove "--" prefix
                    dataVal = int(items[1])
                    for key in self.dataTypes:  ## Loop thru dictionary keys
                        if dataType in key:  ## Check if e.g. "uint16" in key tuple
                            ## Get the TypeSignature tuple
                            typeSig = self.dataTypes[key]
                            break  ## Stop checking dictionary
                    ## If TypeSignature endian is None, get the
                    ## user-provided/default endian. Otherwise get
                    ## the TypeSignature endian
                    endian = typeSig.endian or self.endian
                    ## Convert to bytes of correct length, endianess, and sign
                    dataValB = dataVal.to_bytes(typeSig.byteLen,
                                                byteorder=endian,
                                                signed=typeSig.signed)
                    ## Add data to payload bytearray
                    self.payload.extend(dataValB)
                else:
                    stringParams = items[1].strip("\"").split(
                        ":")  ## e.g. ["16", "ES_APP"]
                    ## Zero init'd bytearray of length e.g. 16
                    fixedLenStr = bytearray(int(stringParams[0]))
                    stringB = stringParams[1].encode(
                    )  ## Param string to bytes
                    ## Insert param bytes into front of bytearray
                    fixedLenStr[:len(stringB)] = stringB
                    ## Add data to payload bytearray
                    self.payload.extend(fixedLenStr)

    def assemblePacket(self):
        self._getOffsets()
        priHeader = self.assemblePriHeader()
        self.packet.extend(priHeader)
        priOffset = bytearray(self.cmdOffsetPri)
        self.packet.extend(priOffset)
        self.cfsCmdSecHdr[0] = self.cmdCode
        secOffset = bytearray(self.cmdOffsetSec)
        for b in b''.join((priHeader, priOffset, self.cfsCmdSecHdr, secOffset,
                           self.payload)):
            self.checksum ^= b
        self.cfsCmdSecHdr[1] = self.checksum
        self.packet.extend(self.cfsCmdSecHdr)
        self.packet.extend(secOffset)
        self.packet.extend(self.payload)
        self.checksum = 0xFF

    def sendPacket(self):
        self.assemblePacket()
        print(f"Data to send: {self.host},{self.port}")

        for i, v in enumerate(self.packet):
            print(f"0x{format(v, '02X')}", end=" ")
            if (i + 1) % 8 == 0:
                print()
        print()
        bytesSent = self.sock.sendto(self.packet, (self.host, self.port))
        return bytesSent > 0

    def _getOffsets(self):
        try:
            self.cmdOffsetPri = 0
            self.cmdOffsetSec = 0
        except ValueError:
            pass        

if __name__ == "__main__":
    
    udata = '35 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
    udataBytes = bytearray.fromhex(udata)    
    mcu = MiniCmdUtil("192.168.0.131", pktID="1C00", userdata=udataBytes)
    sendSuccess = mcu.sendPacket()
    print("Command sent successfully:", sendSuccess)

    # self.mcu = MiniCmdUtil(address, pagePort, pageEndian,
    #                         pagePktId, cmdCodes[idx])
    # sendSuccess = self.mcu.sendPacket()
    # print("Command sent successfully:", sendSuccess)