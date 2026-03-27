#!/usr/bin/env python3
import os, json, glob
from collections import Counter
from datetime import datetime

vault = os.path.expanduser("~/LANIMORPH/vault_templates")
entries = glob.glob(f"{vault}/*.txt")
fingerprints = []

for f in entries:
    with open(f) as fp:
        content = fp.read().strip()
        tokens = tuple(sorted(content.split()))
        fingerprints.append(tokens)

counter = Counter(fingerprints)

out_path = os.path.expanduser("~/LANIMORPH/chain/reports/mirror_mesh_sync.txt")
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, "w") as out:
    out.write("LANIMORPH :: MirrorMesh Sync AI Report\n")
    out.write("Generated: {}\n\n".format(datetime.now()))
    for k, v in counter.items():
        out.write(f"Pattern: {' '.join(k)} — {v}x\n")

print(f"[✓] MirrorMesh AI Sync report saved to: {out_path}")
