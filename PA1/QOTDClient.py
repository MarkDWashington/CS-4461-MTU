import socket, sys

# Make sure we specify an argument
if len(sys.argv) < 2:
    exit()

# Load IP from args
ip = sys.argv[1]

# Create a UDP socket 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

input("Press enter to receive a random quote!")
# Send a packet using the IP specified, port 9876
s.sendto("qotd".encode(), (ip, 9876))
# Wait for a response from the server
data, addr = s.recvfrom(1024)
# Print the data we received
data = data.decode("utf-8")
print(f"Random quote from server: \"{data}\"")