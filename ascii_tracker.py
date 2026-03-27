#!/usr/bin/env python3
import os, datetime
mut_dir = os.path.expanduser("~/LANIMORPH/mutated")
mutants = sorted([f for f in os.listdir(mut_dir) if f.endswith(".sh")])
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(r"""
  _      _         _       _                          __ _           
 | |    (_)       | |     (_)                        / _(_)          
 | |     _ _ __ __| | ___  _ _ __   __ _   ___ _ __ | |_ _  __ _ ___ 
 | |    | | '__/ _` |/ _ \| | '_ \ / _` | / __| '_ \|  _| |/ _` / __|
 | |____| | | | (_| | (_) | | | | | (_| | \__ \ | | | | | | (_| \__ \
 \_____/_|_|  \__,_|\___/|_|_| |_|\__, | |___/_| |_|_| |_|\__, |___/
                                  __/ |                   __/ |    
                                 |___/                   |___/    
""")
print(f"[Time] {ts}\n[Mutant Count] {len(mutants)}\n")
for m in mutants:
    print(f"🧪 {m}")
