

def build_handshake_message(peer_id):
    header = "P2PFILESHARINGPROJ"
    zero_bits = bytes(10)
    peer_id_bytes = peer_id.to_bytes(4, byteorder='big')
    return header.encode() + zero_bits + peer_id_bytes


def build_message(message_type, payload=b''):
    length = len(payload) + 1  # +1 for the message type byte
    return length.to_bytes(4, byteorder='big') + message_type.to_bytes(1, byteorder='big') + payload

def build_choke(): return build_message(0)
def build_unchoke(): return build_message(1)
def build_interested(): return build_message(2)
def build_not_interested(): return build_message(3)

def build_have(piece_index):
    payload = piece_index.to_bytes(4, byteorder='big')
    return build_message(4, payload)

def build_bitfield(bitfield):
    return build_message(5, bitfield)

def build_request(piece_index):
    payload = piece_index.to_bytes(4, byteorder='big')
    return build_message(6, payload)

def build_piece(piece_index, piece_data):
    payload = piece_index.to_bytes(4, byteorder='big') + piece_data
    return build_message(7, payload)
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
