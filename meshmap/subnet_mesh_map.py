#!/usr/bin/env python3
import os, socket
from ipaddress import ip_network
LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")

def draw_ascii_map(log_lines):
    infected = {}
    for line in log_lines:
        if "->" in line:
            ip = line.split("->")[0].split()[-1]
            tag = line.split("::")[-1].strip()
            infected[ip] = tag
    print("=== LANIMORPH :: SUBNET MESH MAP ===")
    net = ip_network("192.168.1.43/24", strict=False)
    for ip in net.hosts():
        ip_str = str(ip)
        tag = infected.get(ip_str, "...")
        print(f"{ip_str:15} | {tag}")

def main():
    if not os.path.exists(LOG): return print("No mutation log.")
    with open(LOG) as f:
        lines = f.readlines()[-50:]
    draw_ascii_map(lines)

if __name__ == "__main__":
    main()
