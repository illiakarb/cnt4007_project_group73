import datetime

def get_time():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    return f"{year}-{month}-{day} {hour}:{minute}:{second}"

def write_log(peer_id, message):
    with open(f"log_peer_{peer_id}.log", 'a') as f:
        f.write(f"[{get_time()}]: {message}\n")


def log_tcp_connection(peer_id_1, peer_id_2):
    message = f"Peer {peer_id_1} makes a connection to Peer {peer_id_2}."
    write_log(peer_id_1, message)

def log_tcp_connection_from(peer_id_1, peer_id_2):
    message = f"Peer {peer_id_1} is connected from Peer {peer_id_2}."
    write_log(peer_id_1, message)

def log_preferred_neighbors(peer_id, preferred_neighbors):
    preferred_neighbors_str = ','.join(str(neighbor) for neighbor in preferred_neighbors)
    message = f"Peer {peer_id} has the preferred neighbors {preferred_neighbors_str}."
    write_log(peer_id, message)

def log_optimistically_unchoked_neighbor(peer_id, optimistically_unchoked_neighbor):
    message = f"Peer {peer_id} has the optimistically unchoked neighbor {optimistically_unchoked_neighbor}."
    write_log(peer_id, message)

def log_unchoking(peer_id_1, peer_id_2):
    message = f"Peer {peer_id_1} is unchoked by {peer_id_2}."
    write_log(peer_id_1, message)

def log_choking(peer_id_1, peer_id_2):
    message = f"Peer {peer_id_1} is choked by {peer_id_2}."
    write_log(peer_id_1, message)

def log_received_have_message(peer_id_1, peer_id_2, piece_index):
    message = f"Peer {peer_id_1} received the ‘have’ message from {peer_id_2} for the piece {piece_index}."
    write_log(peer_id_1, message)

def log_received_interested_message(peer_id_1, peer_id_2):
    message = f"Peer {peer_id_1} received the ‘interested’ message from {peer_id_2}."
    write_log(peer_id_1, message)

def log_received_not_interested_message(peer_id_1, peer_id_2):
    message = f"Peer {peer_id_1} received the ‘not interested’ message from {peer_id_2}."

def log_downloaded_piece(peer_id_1, peer_id_2, piece_index, number_of_pieces):
    message = f"Peer {peer_id_1} has downloaded the piece {piece_index} from {peer_id_2}. Now the number of pieces it has is {number_of_pieces}."
    write_log(peer_id_1, message)

def log_completed_download(peer_id):
    message = f"Peer {peer_id} has downloaded the complete file."
    write_log(peer_id, message)


"""

TCP connection
Whenever a peer makes a TCP connection to other peer, it generates the following log:
[Time]: Peer [peer_ID 1] makes a connection to Peer [peer_ID 2].
[peer_ID 1] is the ID of peer who generates the log, [peer_ID 2] is the peer connected
from [peer_ID 1]. The [Time] field represents the current time, which contains the date,
hour, minute, and second. The format of [Time] is up to you.
Whenever a peer is connected from another peer, it generates the following log:
[Time]: Peer [peer_ID 1] is connected from Peer [peer_ID 2].
[peer_ID 1] is the ID of peer who generates the log, [peer_ID 2] is the peer who has
made TCP connection to [peer_ID 1].
change of preferred neighbors
Whenever a peer changes its preferred neighbors, it generates the following log:
[Time]: Peer [peer_ID] has the preferred neighbors [preferred neighbor ID list].
[preferred neighbor list] is the list of peer IDs separated by comma ‘,’.
change of optimistically unchoked neighbor
Whenever a peer changes its optimistically unchoked neighbor, it generates the following
log:
[Time]: Peer [peer_ID] has the optimistically unchoked neighbor [optimistically
unchoked neighbor ID].
[optimistically unchoked neighbor ID] is the peer ID of the optimistically unchoked
neighbor.
unchoking
Whenever a peer is unchoked by a neighbor (which means when a peer receives an
unchoking message from a neighbor), it generates the following log:
[Time]: Peer [peer_ID 1] is unchoked by [peer_ID 2].
[peer_ID 1] represents the peer who is unchoked and [peer_ID 2] represents the peer
who unchokes [peer_ID 1].
choking
Whenever a peer is choked by a neighbor (which means when a peer receives a choking
message from a neighbor), it generates the following log:
[Time]: Peer [peer_ID 1] is choked by [peer_ID 2].
[peer_ID 1] represents the peer who is choked and [peer_ID 2] represents the peer who
chokes [peer_ID 1].
receiving ‘have’ message
Whenever a peer receives a ‘have’ message, it generates the following log:
[Time]: Peer [peer_ID 1] received the ‘have’ message from [peer_ID 2] for the piece
[piece index].
[peer_ID 1] represents the peer who received the ‘have’ message and [peer_ID 2]
represents the peer who sent the message. [piece index] is the piece index contained in
the message.
receiving ‘interested’ message
Whenever a peer receives an ‘interested’ message, it generates the following log:
[Time]: Peer [peer_ID 1] received the ‘interested’ message from [peer_ID 2].
[peer_ID 1] represents the peer who received the ‘interested’ message and [peer_ID 2]
represents the peer who sent the message.
receiving ‘not interested’ message
Whenever a peer receives a ‘not interested’ message, it generates the following log:
[Time]: Peer [peer_ID 1] received the ‘not interested’ message from [peer_ID 2].
[peer_ID 1] represents the peer who received the ‘not interested’ message and [peer_ID
2] represents the peer who sent the message.
downloading a piece
Whenever a peer finishes downloading a piece, it generates the following log:
[Time]: Peer [peer_ID 1] has downloaded the piece [piece index] from [peer_ID 2]. Now
the number of pieces it has is [number of pieces].
[peer_ID 1] represents the peer who downloaded the piece and [peer_ID 2] represents
the peer who sent the piece. [piece index] is the piece index the peer has downloaded.
[number of pieces] represents the number of pieces the peer currently has.
completion of download
Whenever a peer downloads the complete file, it generates the following log:
[Time]: Peer [peer_ID] has downloaded the complete file.

"""
