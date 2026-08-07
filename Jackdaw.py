#!/usr/bin/env python3
"""Hazel wallpaper daemon.

Cycles the wallpapers of a profile folder, persisting the current wallpaper
(filename, not index) to a JSON file next to this script. Using filenames
keeps the state valid even when the folder is re-sorted, or wallpapers are
added or removed, and the folder is re-scanned every cycle so new images
appear without a restart.

Usage: Hazel.py <profile>
"""

import json
import os
import shutil
import subprocess
import sys
import time

# Root folder containing one subfolder per profile
WALLPAPERS_ROOT = "/home/asrar/Pictures/wallpapers"
# State is stored next to this script, so it works from any cwd
DB_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "wallpaper.json")

SETTER = "awww"  # wallpaper tool (swww v3+ was renamed to awww)
DEFAULT_DELAY = 3600  # seconds between wallpaper changes


def load_state():
    """Load per-profile state, tolerating a missing/corrupt file."""
    try:
        with open(DB_PATH) as f:
            state = json.load(f)
        return state if isinstance(state, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state):
    """Atomic write so a crash mid-write can't corrupt the JSON."""
    tmp = DB_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    os.replace(tmp, DB_PATH)


def scan_wallpapers(folder):
    """Files in folder, newest first."""
    walls = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    walls.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
    return walls


def last_index(stored, walls):
    """Index of the last shown wallpaper, or -1 if unknown.

    Accepts the new filename format and legacy integer-index entries,
    so an existing wallpaper.json keeps working unchanged.
    """
    if isinstance(stored, str):
        try:
            return walls.index(stored)
        except ValueError:
            return -1  # that wallpaper is gone; start from the newest
    try:
        # Legacy entries stored the count before display, i.e. last index + 1
        index = int(stored) - 1
        return index if 0 <= index < len(walls) else -1
    except (TypeError, ValueError):
        return -1


def set_wallpaper(folder, name):
    """Apply a wallpaper without a shell (safe with spaces in filenames)."""
    try:
        subprocess.run([SETTER, "img", os.path.join(folder, name), "--transition-type", "none"])
    except FileNotFoundError:
        sys.exit(f"'{SETTER}' disappeared from PATH - reinstall it and restart Hazel")


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: Hazel.py <profile>")

    profile = sys.argv[1]

    if shutil.which(SETTER) is None:
        sys.exit(f"'{SETTER}' not found in PATH - install it or fix the setter command")

    folder = os.path.join(WALLPAPERS_ROOT, profile)
    if not os.path.isdir(folder):
        sys.exit(f"No wallpaper folder found: {folder}")

    state = load_state()
    index = last_index(state.get(profile), scan_wallpapers(folder))

    try:
        while True:
            walls = scan_wallpapers(folder)
            if not walls:
                # Folder temporarily empty (e.g. files being moved) - retry next cycle
                time.sleep(DEFAULT_DELAY)
                continue

            index = (index + 1) % len(walls)  # advance, wrapping around
            name = walls[index]

            state[profile] = name
            save_state(state)

            print(f"[{profile}] {time.ctime()} -> {name}")
            set_wallpaper(folder, name)

            time.sleep(DEFAULT_DELAY)
    except KeyboardInterrupt:
        print(f"\n[{profile}] stopped - last wallpaper saved to {DB_PATH}")


if __name__ == "__main__":
    main()
