import os, zipfile
from datetime import datetime
from pathlib import Path

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
bundle_name = f"lan_round_bundle_{timestamp}.zip"
bundle_path = Path.home() / "LANIMORPH/exports" / bundle_name
bundle_path.parent.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as z:
    targets = [
        "~/LANIMORPH/chain/inject_silent.log",
        "~/LANIMORPH/chain/replays/lan_chain_replay_dashboard.txt",
        "~/LANIMORPH/chain/replays/lan_subnet_meshmap.txt",
        "~/LANIMORPH/chain/reports/lan_replay_stats.txt",
        "~/LANIMORPH/flyers/latest_flyer.html",
    ]
    for t in targets:
        path = Path(os.path.expanduser(t))
        if path.exists():
            z.write(path, arcname=path.name)
            print(f"[+] Bundled: {path.name}")
print(f"[✓] Final bundle: {bundle_path}")
