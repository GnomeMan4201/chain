#!/usr/bin/env python3
import os, re, curses
from datetime import datetime

LOG_FILE = os.path.expanduser("~/LANIMORPH/chain/mutation_chain.log")

def parse_log():
    entries = []
    if not os.path.exists(LOG_FILE): return entries
    with open(LOG_FILE) as f:
        for line in f:
            m = re.search(r"\[(.*?)\] (.*?) -> (mut_\d+) :: PORT (\d+)", line)
            if m:
                ts, parent, mid, port = m.groups()
                entries.append({
                    "time": ts,
                    "parent": parent,
                    "mutation": mid,
                    "port": port
                })
    return entries[::-1]  # newest first

def draw_tui(stdscr, entries):
    curses.curs_set(0)
    stdscr.nodelay(1)
    max_y, max_x = stdscr.getmaxyx()
    pos = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"LANIMORPH :: Mutation History Viewer ({len(entries)} records)", curses.A_BOLD)

        for i in range(min(max_y - 2, len(entries) - pos)):
            e = entries[pos + i]
            line = f"[{e['time']}] {e['parent']} → {e['mutation']}  :: PORT {e['port']}"
            stdscr.addstr(i+2, 2, line)

        stdscr.addstr(max_y - 1, 0, "[↑/↓] Scroll  [Q] Quit")
        stdscr.refresh()

        key = stdscr.getch()
        if key in [ord('q'), ord('Q')]:
            break
        elif key == curses.KEY_DOWN and pos < len(entries) - (max_y - 2):
            pos += 1
        elif key == curses.KEY_UP and pos > 0:
            pos -= 1

def main():
    entries = parse_log()
    curses.wrapper(draw_tui, entries)

if __name__ == "__main__":
    main()
