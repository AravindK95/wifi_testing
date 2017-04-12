import sys
import socket

srv_addr = socket.gethostbyname("localhost")
srv_port = 8888

class WifiClient():
  SEND = 0  # Spam data to server
  RECV = 1  # Quietly recieve data from server
  ECHO = 2  # Echo data back to server
  dataString = "The Quick Brown Fox Jumped Over The Lazy Dog.\n"

  def __init__(self, host, port, srv_addr, srv_port, mode):
    self.host = host
    self.port = port
    self.srv_addr = srv_addr
    self.srv_port = srv_port
    self.mode = mode
  
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind((self.host, self.port))
    print("Bound to socket " + str(self.host) + ":" + str(self.port))

  def connect(self):
    try:
      self.sock.connect((self.srv_addr, self.srv_port))
      print("Connected to server at "+ str(self.srv_addr) + ":" + str(self.srv_port))

      counter = 0
      while True:
        if self.mode == WifiClient.SEND:
          self.sock.sendall(WifiClient.dataString)
          print("Sending data: "+str(counter))

        elif self.mode == WifiClient.RECV:
          data = self.sock.recv(1024)
          print("Recieved (" + str(counter) + "): " + data.decode())
        
        elif self.mode == WifiClient.ECHO:
          data = self.sock.recv(1024)
          self.sock.sendall(data)
          print("Echoing data (" + str(counter) + "): " + data.decode())

        counter += 1

    finally:
      self.sock.close()

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage: $ python wifi-cli.py ADDR PORT [SRV_ADDR] [SRV_PORT] [MODE]")
    sys.exit(1)
  else:
    host = socket.gethostbyname(sys.argv[1])
    port = int(sys.argv[2])

  if len(sys.argv) > 3:
    srv_addr = socket.gethostbyname(sys.argv[3])

  if len(sys.argv) > 4:
    srv_port = int(sys.argv[4])

  mode = WifiClient.ECHO
  if len(sys.argv) > 5:
    mode_str = sys.argv[5]
    if mode_str == "SEND":
      mode = WifiClient.SEND
    elif mode_str == "RECV":
      mode = WifiClient.RECV
    elif mode_str == "ECHO":
      mode = WifiClient.ECHO
    else:
      print("MODE must be from [SEND, RECV, ECHO]")
      sys.exit(1)

  cli = WifiClient(host, port, srv_addr, srv_port, mode)
  cli.connect()
