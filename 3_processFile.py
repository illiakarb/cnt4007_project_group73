def read_piece(piece_id, piece_sz, f_name, peer_id):
    path = f"peer_{peer_id}/{f_name}"
    with open(path, 'rb') as f:
        f.seek(piece_id * piece_sz)
        return f.read(piece_sz)

def write_piece(piece_id, piece_data, piece_sz, f_name, peer_id):
    path = f"peer_{peer_id}/{f_name}"
    with open(path, 'r+b') as f:
        f.seek(piece_id * piece_sz)
        f.write(piece_data)
