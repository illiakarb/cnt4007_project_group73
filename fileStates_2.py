import os
import math

class FileStates:
    
    '''
    def __init__(self, peer_id, file_name, file_size, piece_size, has_file):
        self.peer_id = peer_id
        self.file_name = file_name
        self.file_size = file_size
        self.piece_size = piece_size
        self.num_pieces = math.ceil(file_size / piece_size)
        self.has_file = has_file

        # create peer dir from passed in peer id, if it doesn't exist
        self.peer_directory = f"peer_{peer_id}"
        os.makedirs(self.peer_directory, exist_ok=True)

        # initialize bitfield based on whether peer has the file or not
        if self.has_file: 
            self.bitfield = [1] * self.num_pieces
        else:
            self.bitfield = [0] * self.num_pieces

        # track which pieces have been requested to avoid duplicate requests
        self.requested_pieces = set()
        if self.has_file:
            self.split_file()

    # split the file into pieces and save them in the peer's directory
    def split_file(self):
        path = os.path.join(self.peer_directory, self.file_name)
        with open(path, "rb") as f:
            for i in range(self.num_pieces):
                pieceData = f.read(self.piece_size)
                piecePath = os.path.join(self.peer_directory, f"piece_{i}")
                with open(piecePath, "wb") as pfile:
                    pfile.write(pieceData)

    # helper functions for piece management
    def get_piecePath(self, piece_index):
        return os.path.join(self.peer_directory, f"piece_{piece_index}")
    
    # check if the peer has a specific piece based on the bitfield
    def has_piece(self, piece_index):
        return self.bitfield[piece_index] == 1
    
    # count how many pieces the peer currently has
    def get_pieceCount(self):
        return sum(self.bitfield)
    
    # read the piece data from disk if the peer has it
    def read_piece(self, piece_index):
        piece_path = self.has_piece(piece_index)
        if piece_path:
            with open(self.get_piecePath(piece_index), "rb") as f:
                return f.read()

    # save a piece to disk and update the bitfield and requested pieces set
    def save_piece(self, piece_index, piece_data):
        if not self.has_piece(piece_index):
            with open(self.get_piecePath(piece_index), "wb") as f:
                f.write(piece_data)
            self.bitfield[piece_index] = 1
            self.requested_pieces.discard(piece_index)
            return True
    
    # mark a piece as requested to avoid duplicate requests
    def mark_piece_requested(self, index):
        self.requested_pieces.add(index)

    # check if a piece has already been requested
    def is_piece_requested(self, index):
        return index in self.requested_pieces

    # determine which pieces the peer is interested in based on another peer's bitfield
    def get_interestingPieces(self, other_bitfield):
        interestingPieces = []
        for i in range(self.num_pieces):
            if other_bitfield[i] == 1 and self.bitfield[i] == 0:
                interestingPieces.append(i)
        return interestingPieces
    
    # check if the peer has all pieces of the file
    def is_complete(self):
        return all(bit == 1 for bit in self.bitfield)
    
    # reconstruct the original file from the pieces once all pieces have been downloaded
    def reconstruct_file(self, output_path):
        with open(output_path, "wb") as f:
            for i in range(self.num_pieces):
                with open(self.get_piecePath(i), "rb") as p:
                    f.write(p.read())
        return True

    '''
    

def __init__(self, numPieces, hasFile=False):
    self.numPieces = numPieces
    self.hasFile = hasFile
   
    if hasFile:
        self.bitfield = [1] * numPieces
    else:
        self.bitfield = [0] * numPieces
    
    self.neighborBitfields = {}
    self.requestedPieces = set()
    # define download here

    def setNeighborBitfield(self, neighbor_id, bitfield):
        self.neighborBitfields[neighbor_id] = bitfield
    
    def updateNeighborPiece(self, neighbor_id, piece_index):
        if neighbor_id not in self.neighborBitfields:
            self.neighborBitfields[neighbor_id] = [0] * self.numPieces
        self.neighborBitfields[neighbor_id][piece_index] = 1
    
    def addPiece(self, piece_index):
        self.bitfield[piece_index] = 1
        self.requestedPieces.discard(piece_index)

    def hasPiece(self, piece_index):
        return self.bitfield[piece_index] == 1
    
    def markRequested(self, piece_index):
        self.requestedPieces.add(piece_index)

    def isRequested(self, piece_index):
        return piece_index in self.requestedPieces

    def getInterestingPieces(self, neighbor_id):
        if neighbor_id not in self.neighborBitfields:
            return []
        
        neighborBitfield = self.neighborBitfields[neighbor_id]
        interestingPieces = []

        for i in range(self.numPieces):
            if neighborBitfield[i] == 1 and self.bitfield[i] == 0:
                interestingPieces.append(i)

        return interestingPieces
    
    def getRequestedPieces(self, neighbor_id):
        if neighbor_id not in self.neighborBitfields:
            return []
        
        neighborBitfield = self.neighborBitfields[neighbor_id]
        requestedPieces = []

        for i in range(self.numPieces):
            if neighborBitfield[i] == 1 and self.bitfield[i] == 0 and not self.isRequested(i):
                requestedPieces.append(i)

        return requestedPieces
    
    # check if the peer has all pieces of the file
    def is_complete(self):
        return all(bit == 1 for bit in self.bitfield)
    
    # implement download logic here