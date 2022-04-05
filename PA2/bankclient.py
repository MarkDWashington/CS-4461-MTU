import socket
import sys

from bankserver import encodePacket, decodePacket


def main():
    # Make sure there are enough args
    if len(sys.argv) < 2:
        print("Usage: bankclient.py <ip>")
        exit()

    # Read in IP, create socket
    ip = sys.argv[1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            # Receive user input
            type = input("Type (BAL, DEP, WTH): ")
            
            if type not in ["BAL", "DEP", "WTH"]:
                print("Invalid type")
                continue
            
            seqNum = 0 if type == "BAL" else int(input("Sequence Number: "))

            amount = 0
            if type != "BAL":
                amount = int(float(input("Amount: ")) * 100)
            
            digits = str(len(str(amount))).zfill(3)

            # Encode a packet
            packet = encodePacket(seqNum, type, digits, amount, seqNum + amount)

            print(f"Sending packet {packet}")

            # Send request
            s.sendto(packet.encode(), (ip, 9876))
            
            # Wait for response if BAL request
            if type == "BAL":
                data, addr = s.recvfrom(32)
                t = decodePacket(data.decode("UTF-8"))
                print(f"Balance: {t._amount}")

        # Handle user killing program
        except KeyboardInterrupt:
            print("User stopped client")
            break

    s.close()
    exit()

if __name__ == "__main__":
    main()
