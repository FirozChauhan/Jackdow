# Jackdaw

A lightweight wallpaper-cycling daemon. Each profile owns a folder of wallpapers; Jackdaw rotates through them on a timer and remembers where it left off — across reboots and even if the folder is re-sorted or images are added/removed.

## Requirements

- A wallpaper setter in `PATH` — `swww` v3+ (renamed to `awww`), configured via `SETTER`
- `python3`

## Setup

1. Put one folder per profile inside `WALLPAPERS_ROOT` (default: `~/Pictures/wallpapers`):

   ```
   ~/Pictures/wallpapers/
   ├── asrar/
   └── bianca/
   ```

2. Start a daemon per profile:

   ```bash
   ./Jackdaw.py asrar
   ```

## How it works

- Scans the profile folder each cycle, so new wallpapers appear without a restart.
- Stores the current wallpaper **by filename** in `wallpaper.json` (next to the script) — surviving re-sorts, additions, and removals.
- Cycles newest-first, one per `DEFAULT_DELAY` (3600s).
- Writes state atomically; safe against crashes mid-write.

## Configuration

Edit the constants at the top of `Jackdaw.py`:

| Constant          | Purpose                                  |
| ----------------- | ---------------------------------------- |
| `WALLPAPERS_ROOT` | Root folder containing profile folders   |
| `SETTER`          | Wallpaper tool to apply images           |
| `DEFAULT_DELAY`   | Seconds between wallpaper changes        |

## License

MIT
