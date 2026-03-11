import socket
import socketserver
import threading
import queue

class Server:
    def __init__(self, host, port: int, msgQueue: queue.Queue, peer_id):
        self.host = host
        self.port = port
        self.peer_id = peer_id
        self.servSocket = None
        self.running = False
        self.thread = None
        self.msgQueue = msgQueue
        self.connections = {}

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.thread.start()

    def listen(self):
        self.servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servSocket.bind((self.host, self.port))
        self.servSocket.listen()

        # print statement
        print(f"Peer {self.peer_id} is listening on {self.host}:{self.port}")

        while self.running:
            try:
                clientSocket, addr = self.servSocket.accept()
                threading.Thread(target=self.handlePeer, args=(clientSocket, addr), daemon=True).start()
            except Exception as e:
                if self.running:
                    print(f"error with listening {e}")

    def handlePeer(self, clientSocket, addr):
        remotePeerID = None
        try:
            handshake = recvExact(clientSocket, 32)
            header, zeroBits, remotePeerID =  parse_handshake_message(handshake)
            
            print(f"Peer {self.peer_id} received handshake from {remotePeerID} at {addr}")

            clientSocket.sendall(build_handshake_message(self.peer_id))

            self.connections[remotePeerID] = clientSocket
            self.msgQueue.put((addr, f"handshake completed with peer {remotePeerID}"))
            
            while self.running:
                data = clientSocket.recv(4096)
                if not data:
                    break
                self.msgQueue.put(("DATA", remotePeerID, data))
        except Exception as e:
            print(f"error handling peer {remotePeerID} at {addr}: {e}")
        finally:
            if remotePeerID in self.connections:
                del self.connections[remotePeerID]
            try:
                clientSocket.close()
            except Exception as e:
                pass

    def stop(self):
        self.running = False
        if self.servSocket:
            try:
                self.servSocket.close()
            except Exception as e:
                pass