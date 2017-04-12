import sys
import socket
import threading

# Host address and port the server binds to
host = socket.gethostbyname("")
port = 8888

class WifiServer():
  SEND = 0  # Spam data to clients
  RECV = 1  # Quietly recieve data from clients
  ECHO = 2  # Echo data back to clients
  dataString = b"The Quick Brown Fox Jumped Over The Lazy Dog.\n"

  def __init__(self, host, port, mode):
    self.host = host
    self.port = port
    self.mode = mode
  
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((self.host, self.port))
    print("Bound to socket " + str(host) + ":" + str(port))

  def listen(self):
    # run "cat /proc/sys/net/ipv4/tcp_max_syn_backlog" to check if SYN queue size supported
    self.sock.listen(16)

    try:
      while True:
        client, address = self.sock.accept()
        print("Connected to client on " + str(address[0]) + ":" + str(address[1]))
        
        client.settimeout(60)
        threading.Thread(target=self.handleClient, args=(client, address, mode)).start()
    
    finally:
      print("closing server...\n")
      self.sock.close()

  def handleClient(self, client, address, mode):
    try:
      counter = 0
      while True:
        if mode == WifiServer.SEND:
          client.sendall(WifiServer.dataString)
          # print("Sending data: "+str(counter))

        elif mode == WifiServer.RECV:
          data = client.recv(1024)
          # print("Received data (" + str(counter) + "): " + data)

        elif mode == WifiServer.ECHO:
          data = client.recv(1024)
          client.sendall(data)
          # print("Echoing data (" + str(counter) + "): " + data)

        counter += 1

    finally:
      print("closing client at " + str(address[0]) +  ":" + str(address[1]))
      client.close()

if __name__ == "__main__":
  mode = WifiServer.SEND

  if len(sys.argv) > 1:
    mode_str = sys.argv[1]
    if mode_str == "SEND":
      mode = WifiServer.SEND
    elif mode_str == "RECV":
      mode = WifiServer.RECV
    elif mode_str == "ECHO":
      mode = WifiServer.ECHO
    else:
      print("MODE must be from [SEND, RECV, ECHO]")
      sys.exit(1)

  srv = WifiServer(host, port, mode)
  srv.listen()
