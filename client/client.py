import ipaddress
import socket
import select
import sys

IP_ADDR = '127.0.0.1'
PORT = 65432


class Client:
    def __init__(self, ip_addr=IP_ADDR, port=PORT) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip_addr, port))

    def run(self):
        run_loop = True
        while run_loop:
            sockets_list = [sys.stdin, self.client]

            read_sockets, write_socket, err_socket = select.select(sockets_list, [], [])
            for socks in read_sockets:
                if socks == self.client:
                    msg = socks.recv(2048)
                    if msg == b'':
                        run_loop = False
                        break
                    print(msg.decode())
                else:
                    msg = sys.stdin.readline()
                    self.client.send(msg.encode())
                    sys.stdout.write('|You|: ')
                    sys.stdout.write(msg)
                    sys.stdout.flush()

        print('Connection closed.')
        self.client.close()


if __name__ == '__main__':
    client = Client()
    client.run()
