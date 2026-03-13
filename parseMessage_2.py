import struct
struct.pack('>I', 5)


def parse_handshake_message(message):
    header_bytes = message[:18]
    header = header_bytes.decode()
    zero_bits = message[18:28]
    peer_id_bytes = message[28:32]
    peer_id = int.from_bytes(peer_id_bytes, byteorder='big')
    return header, zero_bits, peer_id


def parse_message(message):
    len_bytes = message[:4]
    len = int.from_bytes(len_bytes, byteorder='big')
    message_type = message[4]
    payload_start = 5
    payload_len = len - 1
    payload_end = payload_start + payload_len
    payload = message[payload_start:payload_end]
    return message_type, payload


# NOTE VSCODE PROVIDED MESSAGE RECEIPT FUNCTION 