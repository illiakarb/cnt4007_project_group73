# LOGGING UTILITIES FOR THE PEER-TO-PEER FILE SHARING APPLICATION

from datetime import datetime

def peerLog(peer_id, msg):
    logTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Format the log message with the time, peer ID, and msg
    logMsg = f"[{logTime}]: Peer [peer_ID {peer_id}] {msg}.\n"

    # Log the message to the appropriate file
    filename = f"log_peer_{peer_id}.log"

    # Append the log message to the file
    with open(filename, "a") as f:
        f.write(logMsg)

    return