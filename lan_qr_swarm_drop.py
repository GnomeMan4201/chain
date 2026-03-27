#!/usr/bin/env python3
import os, glob
from datetime import datetime
import qrcode

payload_dir = os.path.expanduser("~/LANIMORPH/payloads/mutated")
drop_dir = os.path.expanduser("~/storage/shared/QR_SWARM")
os.makedirs(drop_dir, exist_ok=True)

files = glob.glob(f"{payload_dir}/*.sh")
for i, f in enumerate(files[:10]):
    with open(f) as fp:
        raw = fp.read().strip()
    img = qrcode.make(raw)
    fname = f"qr_payload_{i+1}.png"
    img.save(os.path.join(drop_dir, fname))

print(f"[✓] Generated {len(files[:10])} QR swarm payloads to: {drop_dir}")
