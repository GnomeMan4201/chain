#!/usr/bin/env python3
import os, re
from datetime import datetime
from collections import defaultdict

LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")

def parse_log():
    if not os.path.exists(LOG):
        print("[!] No mutation_chain.log found.")
        return []

    entries = []
    with open(LOG) as f:
        for line in f:
            ts_match = re.search(r"\[(.*?)\]", line)
            ip_match = re.search(r"\] (.*?) ->", line)
            mut_match = re.search(r"-> (.*?) ::", line)
            port_match = re.search(r"PORT (\d+)", line)

            if ts_match and ip_match and mut_match and port_match:
                entries.append({
                    "timestamp": ts_match.group(1),
                    "ip": ip_match.group(1),
                    "mutation": mut_match.group(1),
                    "port": port_match.group(1),
                })
    return sorted(entries, key=lambda x: datetime.strptime(x["timestamp"], "%Y-%m-%d %H:%M:%S"))

def print_ascii(entries):
    print("\n=== LANIMORPH :: Mutation Timeline ===\n")
    print("{:<20} {:<15} {:<12} {:<6}".format("Timestamp", "Host", "Mutation", "Port"))
    print("-" * 58)
    for e in entries:
        print("{:<20} {:<15} {:<12} {:<6}".format(e['timestamp'], e['ip'], e['mutation'], e['port']))

def export_html(entries):
    html = """<html><head><title>Mutation Timeline</title></head><body><h2>LANIMORPH :: Mutation Timeline</h2><table border=1>
<tr><th>Timestamp</th><th>Host</th><th>Mutation</th><th>Port</th></tr>\n"""
    for e in entries:
        html += f"<tr><td>{e['timestamp']}</td><td>{e['ip']}</td><td>{e['mutation']}</td><td>{e['port']}</td></tr>\n"
    html += "</table></body></html>"

    out_path = os.path.expanduser("~/LANIMORPH/chain/mutation_timeline.html")
    with open(out_path, "w") as f:
        f.write(html)
    print(f"[✓] Exported HTML: {out_path}")

def main():
    entries = parse_log()
    if not entries:
        print("[!] No mutation entries found.")
        return
    print_ascii(entries)
    export_html(entries)

if __name__ == "__main__":
    main()
