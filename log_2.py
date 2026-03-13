# LOGGING UTILITIES FOR THE PEER-TO-PEER FILE SHARING APPLICATION

from datetime import datetime

def peerLog(peer_id, msg):
    current_time = datetime.now()
    time_format = "%Y-%m-%d %H:%M:%S"
    logTime = current_time.strftime(time_format)

    # Format the log message with the time, peer ID, and msg
    log_prefix = f"[{logTime}]"
    log_peer = f"Peer [peer_ID {peer_id}]"
    logMsg = f"{log_prefix}: {log_peer} {msg}.\n"

    # Log the message to the appropriate file
    log_prefix_str = "log_peer_"
    log_extension = ".log"
    filename = f"{log_prefix_str}{peer_id}{log_extension}"

    # Append the log message to the file
    with open(filename, "a") as f:
        f.write(logMsg)

    return