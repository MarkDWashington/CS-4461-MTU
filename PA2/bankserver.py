import socket
import itertools


class Transaction:
    def __init__(self, raw: str):
        
        self.sequenceNum = int(raw[:9])
        raw = raw[9:]
        self.type = raw[:3]
        raw = raw[3:]
        self.digits = int(raw[:3])
        raw = raw[3:]
        
        if self.digits > 0:
            self.amount = int(raw[0:(self.digits)]) / 100
            raw = raw[self.digits:]                

        self.checksum = int(raw)

        

class MalformedPacketException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 9876))

    while True:
        try:
            data, addr = s.recvfrom(32)
            data = data.decode("UTF-8")
            t = Transaction(data)
            print(f"Received packet {data}")
        except KeyboardInterrupt:
            print("User stopped server")
            break

    s.close()
    exit()


if __name__ == "__main__":
    main()
