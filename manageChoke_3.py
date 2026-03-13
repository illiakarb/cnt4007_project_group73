import os
import importlib.util
import threading
import random

# load a python file by path
def load_module(module_name, file_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, file_name)
    spec = importlib.util.spec_from_file_location(module_name, full_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# load our files
parse_config_module = load_module("parse_config_module", "parseConfig_1.py")
build_message_module = load_module("build_message_module", "buildMessage_2.py")
log_module = load_module("log_module", "log_2.py")

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
        preferred_neighbors_str = config["NumberOfPreferredNeighbors"]
        unchoking_interval_str = config["UnchokingInterval"]
        optimistic_interval_str = config["OptimisticUnchokingInterval"]
        self.number_of_preferred_neighbors = int(preferred_neighbors_str)
        self.unchoking_interval = int(unchoking_interval_str)
        self.optimistic_unchoking_interval = int(optimistic_interval_str)

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
            is_newly_choked = peer_id not in self.choked_neighbors
            if is_newly_choked:
                self.choked_neighbors[peer_id] = True
            is_new_download = peer_id not in self.download_rates
            if is_new_download:
                self.download_rates[peer_id] = 0

    # remove a neighbor if needed
    def remove_neighbor(self, peer_id):
        peer_id = int(peer_id)
        with self.lock:
            in_interested_neighbors = peer_id in self.interested_neighbors
            if in_interested_neighbors:
                self.interested_neighbors.remove(peer_id)
            in_preferred_neighbors = peer_id in self.preferred_neighbors
            if in_preferred_neighbors:
                self.preferred_neighbors.remove(peer_id)
            in_choked_neighbors = peer_id in self.choked_neighbors
            if in_choked_neighbors:
                del self.choked_neighbors[peer_id]
            in_download_rates = peer_id in self.download_rates
            if in_download_rates:
                del self.download_rates[peer_id]
            is_optimistic_unchoked_neighbor = self.optimistic_unchoked_neighbor == peer_id
            if is_optimistic_unchoked_neighbor:
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

            curr_tot = self.download_rates[peer_id]
            new_tot = curr_tot + num_bytes
            self.download_rates[peer_id] = new_tot


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

    # choose preferred neighbors using interest and download rate
    def recalculate_preferred_neighbors(self):
        with self.lock:
            interested_list = []
            for peer_id in self.interested_neighbors:
                interested_list.append(peer_id)
            # nobody wants our pieces right now
            if len(interested_list) == 0:
                self.preferred_neighbors = set()
                self._apply_choke_states_locked()
                self._reset_download_rates_locked()
                peerLog(self.my_peer_id, "has the preferred neighbors []")
                return

            k = self.number_of_preferred_neighbors
            if k > len(interested_list):
                k = len(interested_list)

            # with the full file, pick preferred neighbors randomly
            if self.has_complete_file:
                random.shuffle(interested_list)
                chosen = interested_list[:k]
            # otherwise pick the interested neighbors with the highest download rate
            else:
                random.shuffle(interested_list)
                interested_list.sort(
                    key=lambda current_peer_id: self.download_rates.get(current_peer_id, 0),
                    reverse=True
                )
                chosen = interested_list[:k]
            self.preferred_neighbors = set(chosen)
            self._apply_choke_states_locked()

            # log the new preferred neighbors
            preferred_list = list(self.preferred_neighbors)
            preferred_list.sort()
            peerLog(self.my_peer_id, f"has the preferred neighbors {preferred_list}")
            # reset interval totals for the next round
            self._reset_download_rates_locked()

    # choose one random interested neighbor that is still choked
    def recalculate_optimistic_unchoked_neighbor(self):
        with self.lock:
            candidates = []
            for peer_id in self.interested_neighbors:
                is_currently_choked = True
                if peer_id in self.choked_neighbors:
                    is_currently_choked = self.choked_neighbors[peer_id]
                is_preferred = peer_id in self.preferred_neighbors

                # only interested and currently choked neighbors can be candidates
                if is_currently_choked and not is_preferred:
                    candidates.append(peer_id)
            old_optimistic = self.optimistic_unchoked_neighbor

            # no valid optimistic neighbor right now
            if len(candidates) == 0:
                self.optimistic_unchoked_neighbor = None
                self._apply_choke_states_locked()
                return
            new_optimistic = random.choice(candidates)
            self.optimistic_unchoked_neighbor = new_optimistic
            self._apply_choke_states_locked()

            # log the new optimistic unchoked neighbor
            if new_optimistic != old_optimistic:
                peerLog(
                    self.my_peer_id,
                    f"has the optimistically unchoked neighbor [{new_optimistic}]"
                )

    # apply choke or unchoke changes from current choices
    def _apply_choke_states_locked(self):
        all_neighbors = set()

        for peer_id in self.choked_neighbors:
            all_neighbors.add(peer_id)

        for peer_id in self.interested_neighbors:
            all_neighbors.add(peer_id)

        for peer_id in all_neighbors:
            should_be_unchoked = False
            if peer_id in self.preferred_neighbors:
                should_be_unchoked = True
            if peer_id == self.optimistic_unchoked_neighbor:
                should_be_unchoked = True
            currently_choked = True
            if peer_id in self.choked_neighbors:
                currently_choked = self.choked_neighbors[peer_id]
            if should_be_unchoked and currently_choked:
                self._send_unchoke_locked(peer_id)
            elif (not should_be_unchoked) and (not currently_choked):
                self._send_choke_locked(peer_id)

    # send a choke message and update local state
    def _send_choke_locked(self, peer_id):
        message_bytes = build_choke()
        self.send_raw_message(peer_id, message_bytes)
        self.choked_neighbors[peer_id] = True

    # send an unchoke message and update local state
    def _send_unchoke_locked(self, peer_id):
        message_bytes = build_unchoke()
        self.send_raw_message(peer_id, message_bytes)
        self.choked_neighbors[peer_id] = False

    # reset download totals after each preferred-neighbor round
    def _reset_download_rates_locked(self):
        for peer_id in self.download_rates:
            self.download_rates[peer_id] = 0