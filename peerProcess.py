import sys
import queue

from parseConfig_1 import parse_common_config, parse_peerinfo
from fileStates_2 import FileStates
from server_4 import Server
from client_4 import Client

def main(): 
    if len(sys.argv) != 2:
        print("usage: python peerProcess.py <peer_id>")
        return
    
    # get peer id from arg
    peer_id = sys.argv[1]

    # parse config files
    commonCFG = parse_common_config()
    peerInfoCFG = parse_peerinfo()

    peer = None
    prevPeers = []

    # get cfg based on arg passed in
    for p in peerInfoCFG:
        if str(p['peer_id']) == peer_id:
            peer = p
            break
        else:
            prevPeers.append(p)

    # if peer is None, print error and exit
    if peer is None:
        print(f"Peer ID {peer_id} not found in PeerInfo.cfg")
        return
    
    # initilize file size, piece size, and num pieces based on common config
    fileSize = int(commonCFG['FileSize'])
    pieceSize = int(commonCFG['PieceSize'])
    # numPieces = math.ceil(fileSize / pieceSize)

    # fileStates = FileStates(numPieces, peer['has_file'])
    
    # print to show its working
    print (f"Peer {peer_id} initialized with host {peer['host_name']} and port {peer['port_number']}.")

    # start server to listen for incoming connections from other peers
    incomingQueue = queue.Queue()
    connections = {}
    listener = Server(peer['host_name'], peer['port_number'], incomingQueue, peer_id, connections)
    listener.start()

    # connect to previous peers in the config file and start listening for messages from them
    client = Client(peer_id, incomingQueue, connections)
    for prev in prevPeers:
        try:
            client.connectToPeer(prev['host_name'], prev['port_number'], prev['peer_id'])
        except Exception as e:
            print(f"error connecting to peer {prev['peer_id']} at {prev['host_name']}:{prev['port_number']}: {e}")
    try:
        while True:
            occured = incomingQueue.get()
            print(f"Peer {peer_id} received message: {occured}")
    except KeyboardInterrupt:
        print("Shutting down server...")
        listener.stop()

if __name__ == "__main__":
    main()



    '''IMPORTANT
    
    TO RUN SET PARAMETER EQUAL TO HOSTING PEER ID
    OPEN ANOTHER TERMINAL FOR EACH PEER AND SET PARAMETER EQUAL TO THAT PEER ID

    or use powershell and run each peer in a separate tab with the appropriate parameter
    '''