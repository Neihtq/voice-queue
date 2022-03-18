import socket
import logging
import threading

HOST = '127.0.0.1'
PORT = 65432

class Server:
    def __init__(self, host=HOST, port=PORT, no_clients=100):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(no_clients)
        self.clients = []
        
    def accept(self):
        while True:
            conn, addr = self.server.accept()
            self.clients.append(conn)
            logging.info(f'{addr[0]} connected')
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()

    def handle_client(self, conn, addr):
        conn.send('Welcome to the chatroom!')

        while True:
            try:
                msg = conn.recv(2048)
                if msg:
                    chat_obj = f'|{addr[0]}|: {msg}'
                    logging.info(chat_obj)
                    
                    # broadcast to all
                    self.broadcast(chat_obj, conn)
                else:
                    # remove connection
                    self.remove(conn) 
            
            except:
                continue

    def broadcast(self, msg, conn):
        for clients in self.clients:
            if clients != conn:
                try:
                    clients.send(msg)
                except:
                    clients.close()


    def remove(self, conn):
        if conn in self.clients:
            self.clients.remove(conn)

    
if __name__ == '__main__':
    server = Server()
    server.accept()