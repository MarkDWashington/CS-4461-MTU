import socket, json, random

quotes = {}
with open("quotes.json", "r") as f: quotes = json.load(f)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 9876))

while True:
    try:
        data, addr = s.recvfrom(4)   
        if data == b"qotd":
            q: str = quotes["quotes"][random.randint(0, len(quotes["quotes"]) - 1)]
            s.sendto(q.encode(), addr)
    except KeyboardInterrupt:
        print("\nUser stopped server")
        break
    except Exception:
        print("Something went wrong :(")
        break