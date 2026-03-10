# Jackdaw 🐦

A lightweight automatic wallpaper changer for Hyprland using `swww`.

## How it works

Jackdaw cycles through wallpapers in a specified folder sorted by last modified date, changing them every 2 minutes. The current wallpaper index is saved to a text file for persistence across restarts.

## Requirements

- `swww` — wallpaper daemon
- `python 3.x`
- Hyprland or any Wayland compositor with swww support

## Setup

1. Edit `app.py` and replace `...yourPath` with your actual paths:

```python
folder = f'...yourPath/{sys.argv[1]}'
dataFolder = f'...yourPath/{sys.argv[2]}.txt'
```

2. Create the data file before first run:

```bash
echo "1" > yourPath/datafilename.txt
```

## Usage

```bash
python app.py <folder_name> <data_file_name>
```

- `<folder_name>` — wallpaper subfolder name inside your wallpapers directory
- `<data_file_name>` — name of the persistence file (no extension needed)

### Example

```bash
python app.py hazel hazel
```

## Autostart with Hyprland

Add to `hyprland.conf`:

```
exec-once = python /yourPath/app.py hazel hazel
```

Or bind to a key:

```
bind = CTRL ALT, W, exec, bash -c "pkill python; python /yourPath/app.py hazel hazel"
```

## Wallpaper folder structure

```
yourPath/
└── hazel/
    ├── wall1.jpg
    ├── wall2.png
    └── wall3.jpeg
```

Wallpapers are sorted by **last modified date** (newest first).

## Configuration

| Option | Location | Default |
|---|---|---|
| Change interval | `time.sleep(120)` | 2 minutes |
| Transition | `--transition-type none` | No transition |
| Sort order | `reverse=True` | Newest first |
