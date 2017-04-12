import sys
import socket

DATA_STRING = "The Quick Brown Fox Jumped Over The Lazy Dog.\n"

def run_server(portnum=8888):
  server_address = ("", portnum)

  # create socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
  try:
    # bind to port
    sock.bind(server_address)
    print("Bound server to socket " + str(server_address[0]) + ":" + str(server_address[1]))

    # listen for connection
    print("Listening for connection...")
    sock.listen(1)

    # handle connection
    while True:
      connection, client_addr = sock.accept()
      counter = 0
      print("Connected to "+str(client_addr))

      try:
        while True:
          connection.sendall(DATA_STRING)

      finally:
        print("Closing connection")
        connection.close()

  finally:
    print("Closing socket")
    sock.close()

if __name__ == "__main__":
  if len(sys.argv) == 2:
    run_server(int(sys.argv[1]))
  else:
    print("Usage:\tpython wifi-server.py PORT_NUMBER")
