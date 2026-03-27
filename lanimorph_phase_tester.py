#!/usr/bin/env python3
import os, time, subprocess
from pathlib import Path

modules = {
    "Beacon Watch": "python3 ~/lan_beacon_watch_silent.py & sleep 2 && pkill -f lan_beacon_watch_silent",
    "Mutator Rotator": "python3 ~/LANIMORPH/chain/lan_mutant_rotator.py",
    "AI Scorer": "python3 ~/LANIMORPH/chain/lan_mutation_scorer.py",
    "QR Flyer": "python3 ~/LANIMORPH/chain/lan_qr_flyer_gen.py",
    "ZIP Encryptor": "LAN_ZIP_PW=banana python3 ~/LANIMORPH/chain/lan_silent_zip_encryptor.py",
    "Mirror Mesh Logger": "python3 ~/LANIMORPH/mesh/log_chain_memory.py 192.168.1.10 testpayload123 42",
    "XOR Diff Map": "python3 ~/LANIMORPH/mesh/mutation_diff_map.py"
}

log_dir = Path("~/LANIMORPH/logs/diagnostic").expanduser()
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir / "phase_test_log.txt"

failures = []
with open(log_path, "w") as log:
    for name, cmd in modules.items():
        log.write(f"\n=== Testing: {name} ===\n")
        print(f"[~] Running {name}...")
        try:
            out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=20)
            log.write(out.decode())
        except subprocess.CalledProcessError as e:
            log.write(f"[!] {name} failed:\n{e.output.decode()}\n")
            failures.append(name)
        except Exception as ex:
            log.write(f"[!] {name} crashed: {ex}\n")
            failures.append(name)

if failures:
    print("\n[!] Failures detected in:")
    for f in failures: print(" -", f)
    print("[*] Please manually inspect log at:", log_path)
else:
    print("\n[✓] All phases passed.")
