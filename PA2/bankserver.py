from typing import Union
import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 9876))

    lastSeqNum = -1
    bal = 23450.00

    print("Server is ready and listening")
    while True:
        try:
            data, addr = s.recvfrom(32)
            data = data.decode("UTF-8")
            print(f"Received packet {data}")

            t = Transaction(data)

            if t._sequenceNum <= lastSeqNum and t._type != "BAL":
                print(f"Invalid sequence number {t._sequenceNum} (last was {lastSeqNum})")
                continue
            elif t._type == "BAL" and t._sequenceNum != 0:
                print(f"Invalid sequence number (should be \"000000000\" for BAL requests")
                continue

            lastSeqNum = t._sequenceNum

            if t._type == "BAL":
                print(f"Balance: ${bal}")
                amount = int(float(bal) * 100)
                digits = str(len(str(amount))).zfill(3)
                s.sendto(encodePacket(lastSeqNum, "BAL", digits, amount, lastSeqNum + amount).encode(), addr)

            elif t._type == "DEP":
                print(
                    f"Deposit request ${bal} + ${t._amount} -> ${bal + t._amount}")
                bal += t._amount

            elif t._type == "WTH":
                print(
                    f"Withdrawal request ${bal} - ${t._amount} -> ${bal - t._amount}")
                bal -= t._amount

        except MalformedPacketException as e:
            print(e)
        except BadChecksumException as e:
            print(e)
        except KeyboardInterrupt:
            print("User stopped server")
            break

    s.close()
    exit()

def encodePacket(sequenceNum: Union[int, str], reqType: str, digits: Union[str, int], amount: Union[str, int], checksum: Union[str, int]) -> str:
    sn: str = ""
    t: str = reqType
    d: str = ""
    a: str = ""
    c: str = ""

    sn = str(sequenceNum)
    sn = sn.zfill(9)

    d = str(digits)
    d = d.zfill(3)
    
    a = str(amount)
    a = a.zfill(3)
    
    c = str(checksum)
    c = c.zfill(9)

    return sn + t + d + a + c
    

def decodePacket(raw: str):
    return Transaction(raw)

class Transaction:
    def __init__(self, raw: str):
        '''Parse a string into a transaction object'''
        try:
            # Parse and validate sequence number
            self._rawSeqNum: str = raw[:9]
            if len(self._rawSeqNum) != 9:
                raise MalformedPacketException("Length of sequence number != 9")
            self._sequenceNum = int(self._rawSeqNum)
            raw = raw[9:]

            # Parse and validate type
            self._rawType: str = raw[:3]
            if self._rawType not in ["BAL", "DEP", "WTH"]:
                raise MalformedPacketException(f"Invalid type \"{self._rawType}\"")
            self._type = self._rawType
            raw = raw[3:]

            # Parse and validate digits
            self._rawDigits: str = raw[:3]
            if len(self._rawDigits) < 3:
                raise MalformedPacketException("Digits not long enough")
            self._digits = int(self._rawDigits)
            raw = raw[3:]

            # Parse and validate amount
            self._rawAmount: str = raw[:max(3, self._digits)]
            if len(self._rawAmount) < 3:
                raise MalformedPacketException("Amount not long enough")
            tempAmount = int(self._rawAmount)
            self._amount: float = tempAmount / 100
            raw = raw[max(3, self._digits):]

            # Parse and validate checksum
            self._rawChecksum: str = raw
            if len(self._rawChecksum) < 9:
                raise MalformedPacketException("Checksum not long enough")
            self._checksum: int = int(self._rawChecksum)

            if self._type == "BAL" and self._rawSeqNum != "000000000":
                raise MalformedPacketException("Sequence number should be \"000000000\" for BAL requests")

            if self._checksum != (tempAmount + self._sequenceNum):
                raise BadChecksumException("Bad checksum")

            print("Checksum validated")

        except Exception as e:
            raise e
        

class MalformedPacketException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class BadChecksumException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


if __name__ == "__main__":
    main()
