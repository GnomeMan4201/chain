#!/usr/bin/env python3
import os
from collections import defaultdict

LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")

def parse_log():
    lineage = defaultdict(list)
    if not os.path.exists(LOG):
        print("[!] No mutation_chain.log found.")
        return lineage

    with open(LOG) as f:
        for line in f:
            if "->" in line:
                parts = line.strip().split("->")
                parent = parts[0].split()[-1]
                child = parts[1].split("::")[0].strip()
                lineage[parent].append(child)
    return lineage

def print_tree(lineage, root=None, depth=0, visited=None):
    if visited is None: visited = set()
    if root is None:
        roots = set(lineage.keys()) - {c for v in lineage.values() for c in v}
        for r in sorted(roots):
            print_tree(lineage, r, depth, visited)
        return

    indent = "  " * depth + "├─" if depth else ""
    print(f"{indent}{root}")
    visited.add(root)

    for child in lineage.get(root, []):
        if child not in visited:
            print_tree(lineage, child, depth + 1, visited)

def main():
    print("\n=== LANIMORPH :: Payload Family Tracker ===\n")
    lineage = parse_log()
    if not lineage:
        print("[!] No lineage data to display.")
    else:
        print_tree(lineage)

if __name__ == "__main__":
    main()
