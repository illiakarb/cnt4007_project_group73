import socket
import sys
import threading

#import build msg and parse msg functions TO DO
from buildMessage_2 import build_handshake_message, recvExact
from parseConfig_1 import parse_common_config, parse_peerinfo
from parseMessage_2 import parse_handshake_message


class Client:
    def __init__(self, peer_id, msgQueue, connections):
        self.peer_id = peer_id
        self.msgQueue = msgQueue
        self.connections = connections

    # connects to a peer at the given host and port, performs handshake, and starts listening for messages from that peer
    def connectToPeer(self, host, port, expectedPeerID):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, int(port)))

        # perform handshake by sending handshake message with own peer ID
        sock.sendall(build_handshake_message(self.peer_id))

        # wait for handshake response and verify peer ID
        resp = recvExact(sock, 32)
        header, zeroBits, remotePeerID = parse_handshake_message(resp)

    
        # error case check
        if int(remotePeerID) != int(expectedPeerID):
            sock.close()
            raise ValueError(f"Expected peer ID {expectedPeerID} but got {remotePeerID}")
        
        self.connections[remotePeerID] = sock
        self.msgQueue.put((f"connected to peer", remotePeerID, (host, port)))
        return

        # threading.Thread(target=self.listenToPeer, args=(sock, remotePeerID), daemon=True).start()
        

    # listens for messages from a connected peer until the connection is closed, then removes the peer from the connections dict
    def listenToPeer(self, socket, remotePeerID):
        try:
            while True:
                # listen for messages until connection is closed
                data = socket.recv(4096)
                if not data:
                    break
                self.msgQueue.put(("DATA", remotePeerID, data))
        # error case
        except Exception as e:
            print(f"error listening to peer {remotePeerID}: {e}")
        finally:
            # remove from connections dict and close socket
            if remotePeerID in self.connections:
                del self.connections[remotePeerID]
            try:
                socket.close()
            except Exception as e:
                pass