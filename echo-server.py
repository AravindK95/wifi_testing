import sys
import socket

server_address = ("", 8888)

def main():
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
          data = connection.recv(4096)

          if data:
            print("Echoing data (" + str(counter) + "): " + str(data))
            counter += 1
            connection.sendall(data)
          else:
            break

      finally:
        print("Closing connection")
        connection.close()

  finally:
    print("Closing socket")
    sock.close()

if __name__ == "__main__":
  main()

