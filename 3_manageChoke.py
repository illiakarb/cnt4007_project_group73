import os
import importlib.util

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
        self.common_cfg_path = common_cfg_path