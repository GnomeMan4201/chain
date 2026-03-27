#!/usr/bin/env python3
import os, time, re

LOG_PATH = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")

def parse_log_line(line):
    match = re.match(r"\[(.*?)\] ([\d.]+) -> (\w+) :: PORT (\d+)", line.strip())
    if match:
        ts, ip, mut_id, port = match.groups()
        return {"time": ts, "ip": ip, "mut_id": mut_id, "port": port}
    return None

def load_chain():
    if not os.path.exists(LOG_PATH):
        print("[-] No mutation log found.")
        return []
    with open(LOG_PATH) as f:
        lines = f.readlines()
    return [parse_log_line(line) for line in lines if parse_log_line(line)]

def draw_timeline(chain):
    print("=== LANIMORPH :: INFECTION TIMELINE ===\n")
    for i, node in enumerate(chain):
        print(f"{i+1:02d}) [{node['time']}]")
        print(f"     ↳ IP: {node['ip']}")
        print(f"     ↳ Mutation ID: {node['mut_id']}")
        print(f"     ↳ Port: {node['port']}")
        print("     " + ("│" if i < len(chain)-1 else "└──") + "\n")

def replay(chain):
    print("=== REPLAY MODE ===")
    for node in chain:
        print(f"[REPLAY] {node['time']} | {node['ip']} injected {node['mut_id']} on port {node['port']}")
        time.sleep(1)

def main():
    chain = load_chain()
    if not chain:
        return
    draw_timeline(chain)
    if input("[?] Replay chain? (y/n): ").lower() == "y":
        replay(chain)

if __name__ == "__main__":
    main()
