import socket, json, random

# FIXME: Add more quotes

print("Server is starting")

# Load quotes from json file and parse to dict
quotes = {}
with open("quotes.json", "r") as f: quotes = json.load(f)

port = 9876

# Create a UDP socket on localhost, port 9876
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 9876))

# Start main loop
print(f"Waiting for connection on port {port}")

while True:
    try:
        print("Server is listening...")
        # Receive four bytes worth of data
        data, addr = s.recvfrom(4)   

        print("Client is connected")

        # Check if data is the "qotd" keyword
        if data == b"qotd":
            print("Client request a quote")

            # Pick a random quote and send it back to the address we received from
            q: str = quotes["quotes"][random.randint(0, len(quotes["quotes"]) - 1)]
            print(f"Sending random quote: \"{q}\"")
            s.sendto(q.encode(), addr)

    except KeyboardInterrupt:
        # Handle keyboard interrupts for clean exits
        print("\nUser stopped server")
        break