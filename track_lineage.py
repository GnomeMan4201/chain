#!/usr/bin/env python3
import os, shutil, time
SRC = os.path.expanduser("~/LANIMORPH/vault/vault_drop.txt")
DST = os.path.expanduser("~/LANIMORPH/chain/lineage")
ts = time.strftime("mut_%Y%m%d_%H%M%S.txt")
shutil.copy(SRC, os.path.join(DST, ts))
print(f"[✓] Payload snapshot saved to: {ts}")
