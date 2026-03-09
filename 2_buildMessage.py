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