#!/usr/bin/env python3
import os, glob, hashlib
from collections import defaultdict
from datetime import datetime

vault = os.path.expanduser("~/LANIMORPH/vault_templates")
hashes = defaultdict(list)

for f in glob.glob(f"{vault}/*.txt"):
    with open(f) as fp:
        content = fp.read()
    h = hashlib.sha256(content.encode()).hexdigest()
    hashes[h].append(os.path.basename(f))

out_path = os.path.expanduser("~/LANIMORPH/chain/reports/mutation_regen_risks.txt")
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, "w") as out:
    out.write("LANIMORPH :: Mutation Regen Tracker\n")
    out.write("Generated: {}\n\n".format(datetime.now()))
    for k, v in hashes.items():
        if len(v) > 1:
            out.write(f"Duplicate hash: {k}\n")
            for item in v:
                out.write(f"  └── {item}\n")

print(f"[✓] Mutation Regen risk report saved to: {out_path}")
