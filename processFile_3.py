def read_piece(piece_id, piece_sz, f_name, peer_id):
    folder = f"peer_{peer_id}"
    path = folder + "/" + f_name
    offset = piece_id * piece_sz
    
    file = open(path, 'rb')
    file.seek(offset)
    data = file.read(piece_sz)
    file.close()
    
    return data

def write_piece(piece_id, piece_data, piece_sz, f_name, peer_id):
    folder = f"peer_{peer_id}"
    path = folder + "/" + f_name
    offset = piece_id * piece_sz
    
    file = open(path, 'r+b')
    file.seek(offset)
    file.write(piece_data)
    file.close()