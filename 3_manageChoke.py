import os
import importlib.util
import threading

# load a python file by path
def load_module(module_name, file_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, file_name)
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# load our files
parse_config_module = load_module("parse_config_module", "1_parseConfig.py")
build_message_module = load_module("build_message_module", "2_buildMessage.py")
log_module = load_module("log_module", "2_log.py")

# use helper functions from the files
parse_common_config = parse_config_module.parse_common_config
build_choke = build_message_module.build_choke
build_unchoke = build_message_module.build_unchoke
peerLog = log_module.peerLog

class ChokeManager:
    # choke manager for one peer
    def __init__(self, my_peer_id, send_raw_message, common_cfg_path="Common.cfg"):
        self.my_peer_id = int(my_peer_id)
        self.send_raw_message = send_raw_message

        # read choke values from Common.cfg
        config = parse_common_config(common_cfg_path)
        self.number_of_preferred_neighbors = int(config["NumberOfPreferredNeighbors"])
        self.unchoking_interval = int(config["UnchokingInterval"])
        self.optimistic_unchoking_interval = int(config["OptimisticUnchokingInterval"])

        # store neighbor state
        self.interested_neighbors = set()
        self.preferred_neighbors = set()
        self.optimistic_unchoked_neighbor = None

        # True means we are choking that neighbor
        self.choked_neighbors = {}

        # bytes downloaded from each neighbor during this interval
        self.download_rates = {}

        # if we already have the full file, preferred neighbors are random
        self.has_complete_file = False

        # thread and lock setup
        self.running = False
        self.lock = threading.Lock()
        self.preferred_thread = None
        self.optimistic_thread = None

    # add a neighbor and start them as choked
    def add_neighbor(self, peer_id):
        peer_id = int(peer_id)
        with self.lock:
            if peer_id not in self.choked_neighbors:
                self.choked_neighbors[peer_id] = True
            if peer_id not in self.download_rates:
                self.download_rates[peer_id] = 0

    # remove a neighbor if needed
    def remove_neighbor(self, peer_id):
        peer_id = int(peer_id)
        with self.lock:
            if peer_id in self.interested_neighbors:
                self.interested_neighbors.remove(peer_id)
            if peer_id in self.preferred_neighbors:
                self.preferred_neighbors.remove(peer_id)
            if peer_id in self.choked_neighbors:
                del self.choked_neighbors[peer_id]
            if peer_id in self.download_rates:
                del self.download_rates[peer_id]
            if self.optimistic_unchoked_neighbor == peer_id:
                self.optimistic_unchoked_neighbor = None

    # update whether this peer has the full file
    def set_has_complete_file(self, has_complete_file):
        with self.lock:
            self.has_complete_file = bool(has_complete_file)

    # record that a neighbor wants pieces from us
    def mark_interested(self, peer_id):
        peer_id = int(peer_id)

        with self.lock:
            self.interested_neighbors.add(peer_id)
            if peer_id not in self.choked_neighbors:
                self.choked_neighbors[peer_id] = True
            if peer_id not in self.download_rates:
                self.download_rates[peer_id] = 0

    # record that a neighbor does not need pieces from us
    def mark_not_interested(self, peer_id):
        peer_id = int(peer_id)
        with self.lock:
            if peer_id in self.interested_neighbors:
                self.interested_neighbors.remove(peer_id)

    # update download amount so we can rank neighbors later
    def record_download(self, peer_id, num_bytes):
        peer_id = int(peer_id)
        num_bytes = int(num_bytes)
        with self.lock:
            if peer_id not in self.download_rates:
                self.download_rates[peer_id] = 0

            self.download_rates[peer_id] = self.download_rates[peer_id] + num_bytes

    # get the current preferred neighbors
    def get_preferred_neighbors(self):
        with self.lock:
            result = list(self.preferred_neighbors)
            result.sort()
            return result

    # get the current optimistic neighbor
    def get_optimistic_neighbor(self):
        with self.lock:
            return self.optimistic_unchoked_neighbor

    # check if we are currently choking a neighbor
    def is_choking_neighbor(self, peer_id):
        peer_id = int(peer_id)
        with self.lock:
            if peer_id not in self.choked_neighbors:
                return True
            return self.choked_neighbors[peer_id]