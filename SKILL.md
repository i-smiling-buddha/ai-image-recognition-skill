---
name: transparent-png-check
description: Use whenever a PNG/WebP/GIF image is attached or referenced and its transparency matters (mascots, logos, stickers, cutouts) — verify the alpha channel with code instead of trusting vision.
---

# Transparent PNG Check

## Why
When an image is shown to Claude visually, its alpha channel is usually flattened onto white or black. Transparent areas then *look* like a background. Never judge transparency by eye — always check the actual pixel data.

## When to use
- User attaches a PNG/WebP/GIF of a mascot, logo, sticker, character or cutout
- User asks "is this transparent?", "does it have a background?", or wants it placed on a website/app/merch
- Before compositing, resizing, or putting an image on a colored background

## Steps
1. Find the file (attachment by name, or the path the user gave). Work on a copy, never the original.
2. Run `python3 scripts/check_png.py <file1> [file2 ...]` from this skill's folder (install Pillow with `pip install --break-system-packages pillow` if missing).
3. Open the generated `*_on_magenta.png` preview to see the real cutout — magenta areas = truly transparent.
4. Report to the user in plain words:
   - Whether an alpha channel exists
   - % fully transparent / semi-transparent / opaque
   - Subject bounding box (useful for cropping)
   - If FAKE transparency (checkerboard baked into pixels) was detected, say so clearly and suggest a real background-removal step.
   - If alpha exists but every pixel is opaque, say the image effectively still has a background.
5. When later describing or editing the image, treat transparent pixels as "no background" — never describe them as white/black/checkered.

## Notes
- Checkerboard detection is a heuristic (gray/white alternating squares in corners). If unsure, look at the magenta preview — a fake PNG will show no magenta at all.
- JPG files never have transparency; say so directly.
- Reply in the user's preferred language.
