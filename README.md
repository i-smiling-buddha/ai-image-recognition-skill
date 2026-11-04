# transparent-png-check

A [Claude](https://claude.ai) skill that checks whether a PNG / WebP / GIF image is **really transparent**, using code instead of vision.

## The problem
When an image is shown to an AI model visually, the alpha channel usually gets flattened onto a white or black background. The model then "sees" a background that isn't there, or it gets fooled by **fake transparent PNGs**, where the grey-white checkerboard is baked into the pixels.

## What this skill does
- Reads the actual alpha channel with Pillow
- Reports % fully transparent / semi-transparent / opaque pixels
- Gives the subject's bounding box (handy for cropping)
- Detects fake checkerboard "transparency"
- Saves previews composited on **magenta** and **black**, so the real cutout is easy to see

## Install
**Claude app:** download this repo as a ZIP and upload it under *Settings → Capabilities → Skills*.
**Claude Code:** copy the folder into `~/.claude/skills/transparent-png-check/`.

## Use the script directly
```bash
pip install pillow
python3 scripts/check_png.py mascot.png logo.png
```

Example output:
```
File: mascot.png
Size: 200x200  Mode: RGBA
Alpha channel: HAI
Fully transparent: 80.0%  Semi-transparent: 0.0%  Opaque: 20.0%
Subject bounding box (alpha>0): (50, 50, 151, 151)
Preview: ./mascot_on_magenta.png
Preview: ./mascot_on_black.png
```

## License
MIT. Made by **Smiling Buddha** · Chandoriya Technology
