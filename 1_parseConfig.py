def parse_common_config(filepath="Common.cfg"):
    config = {}
    with open(filepath, "r") as f:
        config = {}
        for line in f:
            key, value = line.split()
            config[key] = value
    return config

if __name__ == "__main__":
    config = parse_common_config()
    print(config)