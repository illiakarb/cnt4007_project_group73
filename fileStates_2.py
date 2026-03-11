import os
import math

class FileStates:
    def __init__(self, numPieces, hasFile=False):
        self.numPieces = numPieces
        self.hasFile = hasFile
    
        # initialize bitfield to all 1s if has file, otherwise all 0s
        if hasFile:
            self.bitfield = [1] * numPieces
        else:
            self.bitfield = [0] * numPieces
        
        self.neighborBitfields = {}
        self.requestedPieces = set()
        # define download here

        # set neightbor bitfield for a peer
        def setNeighborBitfield(self, neighbor_id, bitfield):
            self.neighborBitfields[neighbor_id] = bitfield
        
        # update neighbor bitfield when receiving have message from neighbor
        def updateNeighborPiece(self, neighbor_id, piece_index):
            if neighbor_id not in self.neighborBitfields:
                self.neighborBitfields[neighbor_id] = [0] * self.numPieces
            self.neighborBitfields[neighbor_id][piece_index] = 1
        
        # update own bitfield when receiving piece data and mark piece as no longer requested
        def addPiece(self, piece_index):
            self.bitfield[piece_index] = 1
            self.requestedPieces.discard(piece_index)

        # check if the peer has a specific piece
        def hasPiece(self, piece_index):
            return self.bitfield[piece_index] == 1
        
        # mark a piece as requested to avoid requesting the same piece multiple times from different neighbors
        def markRequested(self, piece_index):
            self.requestedPieces.add(piece_index)

        # check if a piece is already requested
        def isRequested(self, piece_index):
            return piece_index in self.requestedPieces

        # get list of pieces that a neighbor has and the peer does not have
        def getInterestingPieces(self, neighbor_id):
            if neighbor_id not in self.neighborBitfields:
                return []
            
            neighborBitfield = self.neighborBitfields[neighbor_id]
            interestingPieces = []

            for i in range(self.numPieces):
                if neighborBitfield[i] == 1 and self.bitfield[i] == 0:
                    interestingPieces.append(i)

            return interestingPieces
        
        # get list of pieces that a neighbor has, the peer does not have, and has not already requested
        def getRequestedPieces(self, neighbor_id):
            if neighbor_id not in self.neighborBitfields:
                return []
            
            neighborBitfield = self.neighborBitfields[neighbor_id]
            requestedPieces = []

            # iterate over numPieces and check if neighbor has piece, peer does not have piece, and piece is not already requested
            for i in range(self.numPieces):
                if neighborBitfield[i] == 1 and self.bitfield[i] == 0 and not self.isRequested(i):
                    requestedPieces.append(i)

            return requestedPieces
        
        # check if the peer has all pieces of the file
        def is_complete(self):
            return all(bit == 1 for bit in self.bitfield)
        
        # implement download logic here