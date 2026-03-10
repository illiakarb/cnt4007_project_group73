import struct
struct.pack('>I', 5)


def parse_handshake_message(message):
    header = message[:18].decode()
    zero_bits = message[18:28]
    peer_id = int.from_bytes(message[28:32], byteorder='big')
    return header, zero_bits, peer_id

def parse_message(message):
    length = int.from_bytes(message[:4], byteorder='big')
    message_type = message[4]
    payload = message[5:5+length-1]  # -1 for the message type byte
    return message_type, payload


//  NOTE VSCODE PROVIDED MESSAGE RECEIPT FUNCTION 


