---
name: image-recognition
description: Use whenever an image file is attached or referenced and its real properties matter — transparency, true format, size/DPI, colors, blur, blank images, EXIF/GPS — verify with code instead of trusting vision alone.
---

# Image Recognition

## Why
When an image is shown to Claude visually, a lot of real information is lost or distorted:
- The alpha channel is flattened onto white/black, so transparent areas *look* like a background.
- Exact pixel size, DPI, file format, color profile and EXIF/GPS metadata are invisible.
- Downscaled previews hide blur, compression and tiny details.

So for anything factual about an image, check the file itself with code, then use vision for *what the image shows*.

## When to use
- An image (PNG, JPG, WebP, GIF, BMP, TIFF) is attached or a path is given, and the user asks about it or wants it used somewhere (website, app, Play Store, print, merch, Shopify)
- Questions like "is this transparent?", "what size is it?", "is it good enough to print?", "is this blurry?", "what colors does it use?", "does it have location data?"
- Before resizing, compositing, cropping, uploading, or putting an image on a colored background

## Steps
1. Locate the file (attachment by name, or the user's path). Work on a copy, never the original.
2. Run the inspector from this skill's folder. Use an existing virtual environment or create and activate one with `python -m venv .venv`, then install Pillow with `python -m pip install pillow` (numpy is optional). Avoid installing packages into system Python.
   `python scripts/inspect_image.py <file1> [file2 ...] --out <scratch-dir>`
   Use `python3` instead of `python` if that is the Python 3 command on your system. Add `--json` for machine-readable output.
3. Open `<name>_on_magenta.png` from the output folder to see the real cutout — magenta = truly transparent.
4. Combine the script facts with a visual look at the image, then answer in plain words. Lead with what the user asked; mention other findings only if they matter:
   - **Transparency verdict**: REAL / NOT transparent / FAKE (checkerboard baked in) / alpha unused
   - **True format** — flag if the extension doesn't match (e.g. a PNG saved as .jpg)
   - **Size, aspect ratio, DPI**, and print size at 300 DPI when print/merch is involved
   - **Dominant colors** as hex codes (useful for brand palettes)
   - **Sharpness hint** — warn if likely blurry/soft
   - **Blank/solid image** warning
   - **Animated** frame count for GIF/WebP
   - **EXIF**: camera/software; if **GPS is present**, warn that the photo contains location data before it's shared publicly
5. When describing or editing the image afterwards, trust the script over vision: never call transparent pixels "white background" or a checkerboard "transparent".

## Notes
- Checkerboard detection and the sharpness score are heuristics — confirm with the previews when it matters.
- JPG never has transparency; say so directly.
- Reply in the user's preferred language.
