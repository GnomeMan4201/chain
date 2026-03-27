#!/usr/bin/env python3
import random, time
print("\n🔥  LANIMORPH :: LAN HEATMAP\n")
for i in range(1, 30):
    status = "[ INFECTED ]" if i % 3 == 0 else "[  CLEAN  ]"
    print(f" 192.168.0.{i:<3} ↬ {status}")
    time.sleep(0.1)
input("\n[Press Enter to return to dashboard]")
