#!/usr/bin/env python3
import os
LOG = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")
def build_tree():
    if not os.path.exists(LOG): return print("No mutation log.")
    tree = {}
    with open(LOG) as f:
        for line in f:
            parts = line.strip().split()
            if "->" in parts and "::" in parts:
                parent = parts[1]
                child = parts[3]
                port = parts[-1]
                tree.setdefault(parent, []).append((child, port))
    print("=== LANIMORPH :: MUTATION FAMILY TREE ===")
    for parent, children in tree.items():
        print(f"{parent}")
        for child, port in children:
            print(f"  └── {child} @ {port}")
if __name__ == "__main__":
    build_tree()
