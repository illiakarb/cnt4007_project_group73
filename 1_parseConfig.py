# PARSES FILE INFORMATION TO COMMON.CFG, SIMPLE INITIALIZATION FILE 

def parse_common_config(filepath="Common.cfg"):
    config = {}
    with open(filepath, "r") as file:
        for line in file:
            key, value = line.split()
            config[key] = value
    return config

def parse_peerinfo(filepath="PeerInfo.cfg"):
    peers = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.split()
            peer = {
                'peer_id': parts[0],
                'host_name': parts[1],
                'port_number': int(parts[2]),
                'has_file': parts[3] == '1'
            }
            peers.append(peer)
    return peers

if __name__ == "__main__":
    config = parse_common_config()
    peers = parse_peerinfo()

    print(config)
    print(peers)