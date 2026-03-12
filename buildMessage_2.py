def build_handshake_message(peer_id):
    header = "P2PFILESHARINGPROJ"
    header_bytes = header.encode()

    zero_bits = bytes(10)

    peer_id_int = int(peer_id)
    peer_id_bytes = peer_id_int.to_bytes(4, byteorder='big')

    message = header_bytes + zero_bits + peer_id_bytes
    return message

def build_message(message_type, payload=b''):
    payload_len = len(payload)
    message_type_byte_len = 1
    total_len = payload_len + message_type_byte_len

    len_bytes = total_len.to_bytes(4, byteorder='big')
    type_bytes = message_type.to_bytes(1, byteorder='big')

    message = len_bytes + type_bytes + payload
    return message

def build_choke():
    return build_message(0)

def build_unchoke():
    return build_message(1)

def build_interested():
    return build_message(2)

def build_not_interested():
    return build_message(3)

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

# receive exact n bytes from a socket, handling cases where recv may return less than n bytes
def recvExact(sock, n):
    # keep receiving until we have received n bytes
    data = b''
    while len(data) < n:
        # receive the remaining bytes
        packet = sock.recv(n - len(data))
        if not packet:
            raise ConnectionError("socket closed before receiving data")
        data += packet
    return data

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