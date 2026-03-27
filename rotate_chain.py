#!/usr/bin/env python3
import os, time
from dna_mutator import main as mutate
print("[✓] Rotating mutation chain every 30 seconds. Press Ctrl+C to stop.")
while True:
    os.system("clear")
    print("=== LANIMORPH :: CHAIN ROTATOR ===")
    mutate()
    time.sleep(30)
