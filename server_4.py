import socket
import threading
import queue

from buildMessage_2 import build_handshake_message
from buildMessage_2 import recvExact
from parseMessage_2 import parse_handshake_message

class Server:
    def __init__(self, host, port: int, msgQueue: queue.Queue, peer_id, connections):
        self.host = host
        self.port = port
        self.peer_id = peer_id
        self.servSocket = None
        self.running = False
        self.thread = None
        self.msgQueue = msgQueue
        self.connections = connections

    # starts the server thread to listen for incoming connections
    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.thread.start()

        # listen for incoming connections and handle them in separate threads
    def listen(self):
        addr_family = socket.AF_INET
        sock_type = socket.SOCK_STREAM
        self.servSocket = socket.socket(addr_family, sock_type)
        self.servSocket.bind((self.host, self.port))
        self.servSocket.listen()

        # print to show its working
        print(f"Peer {self.peer_id} is listening on {self.host}:{self.port}")

        # accept incoming connections and handle them in separate threads
        while self.running:
            try:
                clientSocket, addr = self.servSocket.accept()
                threading.Thread(target=self.handlePeer, args=(clientSocket, addr), daemon=True).start()
            except Exception as e:
                if self.running:
                    print(f"error with listening {e}")

    # handles incoming connection from a peer, performs handshake, and listens for messages until the connection is closed
    def handlePeer(self, clientSocket, addr):
        remotePeerID = None
        try:
            # perform handshake
            handshake = recvExact(clientSocket, 32)
            header, zeroBits, remotePeerID =  parse_handshake_message(handshake)
            
            # print to show its working
            print(f"Peer {self.peer_id} received handshake from {remotePeerID} at {addr}")

            # send handshake response
            clientSocket.sendall(build_handshake_message(self.peer_id))

            # add to connections dict and msg queue
            self.connections[remotePeerID] = clientSocket
            self.msgQueue.put((addr, f"handshake completed with peer {remotePeerID}"))
            
            # listen for messages until connection is closed
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

    # stops the server and closes the socket
    def stop(self):
        self.running = False
        if self.servSocket:
            try:
                self.servSocket.close()
            except Exception as e:
                pass