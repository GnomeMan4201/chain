import json
from collections import defaultdict

log_path = "/data/data/com.termux/files/home/LANIMORPH/logs/inject_silent.log"

nodes = {}
edges = []
infected = set()
depth_map = {}

with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = [l.strip() for l in f.readlines() if l.strip() and "Host compromised by" in l]

for line in lines:
    try:
        parts = line.split("silent: Host compromised by ")
        receiver = parts[0].split("]")[-1].strip()
        sender = parts[1].split(" [")[0].strip()
        infected.add(receiver)
        infected.add(sender)
        edges.append((sender, receiver))
    except Exception:
        continue

def calc_depths():
    depth = defaultdict(lambda: -1)
    root = "127.0.0.1"
    depth[root] = 0
    for _ in range(10):
        for src, dst in edges:
            if depth[src] != -1:
                depth[dst] = max(depth[dst], depth[src] + 1)
    return depth

depth_map = calc_depths()

def gen_color(level):
    return {
        0: "#88ff88",
        1: "#ffff88",
        2: "#ffcc66",
        3: "#ff8888",
        4: "#cc66cc",
    }.get(level, "#aaaaaa")

node_data = [
    {
        "id": ip,
        "label": ip,
        "color": gen_color(depth_map.get(ip, -1)),
    }
    for ip in infected
]

edge_data = [{"from": src, "to": dst} for src, dst in edges]

output = {
    "nodes": node_data,
    "edges": edge_data,
    "stats": {
        "total_hosts": len(infected),
        "max_depth": max(depth_map.values(), default=0)
    }
}

with open("map_data.json", "w") as f:
    json.dump(output, f, indent=2)
