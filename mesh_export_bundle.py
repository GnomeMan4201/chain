#!/usr/bin/env python3
import os, shutil, zipfile
from datetime import datetime
from pathlib import Path
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
bundle_dir = Path(f"~/LANIMORPH/mesh_bundles/mesh_{ts}").expanduser()
bundle_dir.mkdir(parents=True, exist_ok=True)
# Copy all relevant logs
shutil.copy(os.path.expanduser("~/LANIMORPH/logs/silent/inject_silent.log"), bundle_dir / "inject_silent.log")
shutil.copy(os.path.expanduser("~/LANIMORPH/logs/mirror/mirror_history.json"), bundle_dir / "mirror_history.json")
# Zip it
zip_path = bundle_dir.with_suffix(".zip")
with zipfile.ZipFile(zip_path, "w") as z:
    for f in bundle_dir.glob("*"):
        z.write(f, arcname=f.name)
print("[+] Mesh export ready:", zip_path)
