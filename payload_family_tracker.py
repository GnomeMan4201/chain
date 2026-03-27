#!/usr/bin/env python3
import os, json, re
from collections import defaultdict

LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")
FAMILY_DB = os.path.expanduser("~/LANIMORPH/chain/payload_family.json")

def parse_log():
    families = defaultdict(list)
    if not os.path.exists(LOG): return families

    with open(LOG) as f:
        for line in f:
            line = line.strip()
            if "::" in line:
                parts = line.split("::")
                timestamp = line.split("]")[0].strip("[")
                ip_mut = parts[0].split("->")
                if len(ip_mut) == 2:
                    ip, mut_id = ip_mut
                    mut_id = mut_id.strip()
                    port = parts[1].replace("PORT", "").strip()
                    origin = detect_origin(mut_id)
                    families[origin].append({
                        "mutation": mut_id,
                        "ip": ip.strip(),
                        "timestamp": timestamp,
                        "port": port
                    })
    return families

def detect_origin(mut_id):
    # Extract the mutation number and infer approximate ancestry
    try:
        num = int(re.search(r"(\d+)", mut_id).group(1))
        if num < 2000: return "wifi_creds_dump"
        if num < 4000: return "dns_leak"
        if num < 6000: return "recon_probe"
        if num < 8000: return "scout_ping"
        return "unknown"
    except: return "unknown"

def save_tree(families):
    with open(FAMILY_DB, "w") as f:
        json.dump(families, f, indent=2)
    print(f"[✓] Payload family tree written to: {FAMILY_DB}")

def print_summary(families):
    print("\n== Payload Mutation Families ==")
    for origin, nodes in families.items():
        print(f"[{origin}] → {len(nodes)} mutations")
        for n in nodes[-3:]:  # show latest 3
            print(f"   ↳ {n['mutation']} @ {n['timestamp']} from {n['ip']}")

if __name__ == "__main__":
    tree = parse_log()
    save_tree(tree)
    print_summary(tree)
