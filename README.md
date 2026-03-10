# Jackdaw 🐦

A simple automatic wallpaper changer for Hyprland using `swww`.

## How it works

Jackdaw cycles through wallpapers in a specified folder, changing them at a set interval. It remembers the last wallpaper index using a data file, so it picks up where it left off after restart.

## Requirements

- `swww` — wallpaper daemon
- `python` — 3.x
- Hyprland (or any wayland compositor with swww support)

## Usage

```bash
python app.py <folder_name> <data_file_name>
```

- `<folder_name>` — name of the wallpaper subfolder inside `~/Pictures/wallpapers/`
- `<data_file_name>` — name of the data file to store wallpaper index (no extension)

### Example

```bash
python app.py hazel hazel
```

This will:
- Look for wallpapers in `/home/asrar/Pictures/wallpapers/hazel/`
- Store the current index in `/home/asrar/code/Jackdaw/scripts/hazel.txt`

## Autostart with Hyprland

Add to `hyprland.conf`:

```
exec-once = python /home/asrar/code/Jackdaw/scripts/app.py hazel hazel
```

Or bind to a key:

```
bind = CTRL ALT, W, exec, python /home/asrar/code/Jackdaw/scripts/app.py hazel hazel
```

## Wallpaper folder structure

```
~/Pictures/wallpapers/
└── hazel/
    ├── wall1.jpg
    ├── wall2.png
    └── wall3.jpeg
```

## Configuration

Edit these values inside `app.py`:

| Variable | Description |
|---|---|
| `folder` | Path to wallpaper directory |
| `dataFolder` | Path to index data file |
| `time.sleep(120)` | Change interval in seconds (default: 2 min) |
