#!/usr/bin/env python3
import os, re, socket

LOG = os.path.expanduser("~/LANIMORPH/chain/inject_silent.log")
LOCAL = socket.gethostbyname(socket.gethostname())

def parse_log():
    entries = {}
    if not os.path.exists(LOG):
        print("[!] No inject_silent.log found.")
        return entries

    with open(LOG) as f:
        for line in f:
            match = re.match(r"\[(.*?)\] (\d+\.\d+\.\d+\.\d+) -> (.*?) :: PORT (\d+)", line)
            if match:
                _, host, mut_id, port = match.groups()
                entries[host] = (mut_id, port)
    return entries

def ip_to_last_octet(ip):
    return int(ip.strip().split('.')[-1])

def render_grid(entries):
    print("\n=== LANIMORPH :: Subnet Mesh Infection Map ===\n")
    grid = [""] * 16  # 16 rows of 16 IPs = 256 IPs

    for i in range(256):
        ip = f"192.168.0.{i}"
        row = i // 16
        if ip in entries:
            mut_id, port = entries[ip]
            symbol = "🧬"
        elif ip == LOCAL:
            symbol = "📍"
        else:
            symbol = "·"
        grid[row] += f"{symbol} "

    for row in grid:
        print(row)
    print("\nLegend: 🧬 Infected  📍 Self  · Unused")
    print(f"Total infected: {len(entries)}")
