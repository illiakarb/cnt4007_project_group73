def build_handshake_message(peer_id):
    header = "P2PFILESHARINGPROJ"
    zero_bits = bytes(10)
    peer_id_bytes = peer_id.to_bytes(4, byteorder='big')
    return header.encode() + zero_bits + peer_id_bytes

def receive_handshake_message(message):
    header = message[:18].decode()
    zero_bits = message[18:28]
    peer_id = int.from_bytes(message[28:32], byteorder='big')
    return header, zero_bits, peer_id

def build_message(message_type, payload=b''):
    length = len(payload) + 1  # +1 for the message type byte
    return length.to_bytes(4, byteorder='big') + message_type.to_bytes(1, byteorder='big') + payload

def receive_message(message):
    length = int.from_bytes(message[:4], byteorder='big')
    message_type = message[4]
    payload = message[5:5+length-1]  # -1 for the message type byte
    return message_type, payload

'''
HANDSHAKE MESSAGE: 32 bytes
    header: 18 byte string
    zero bits: 10 bytes of zeros
    peer id: 4 byte integer

ACTUAL MESSAGE: 
    length: 4 byte integer
    type: 1 byte integer
    payload: variable length, depending on message type

PAYLOADS
    choke, unchoke, interested, not interested: no payload
    have: 4 byte integer (piece index)
    bitfield: variable length bitfield
    request: 4 byte payload
    piece: 4 byte piece index + variable length piece data
'''
