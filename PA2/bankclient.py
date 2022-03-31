import socket
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: bankclient.py <ip>")
        exit()

    ip = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sequenceNum: int = int(input("Sequence number: "))
    type: str = input("Type (BAL, WTH, DEP): ")
    amount: str = 0

    if type != "BAL":
        amount = int(float(input("Amount: ")) * 100)

    checksum = str(sequenceNum * 100 + amount)

    packet = sequenceNum.zfill(9) + type + str(len(amount)).zfill(3) + amount + checksum
    print(f"Sending packet {packet}")

    s.sendto(packet.encode(), (ip, 9876))

if __name__ == "__main__":
    main()