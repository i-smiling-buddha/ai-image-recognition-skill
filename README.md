# ai-image-recognition (Claude skill)

A [Claude](https://claude.ai) skill that makes Claude **recognise an image's real properties from the file itself**, instead of guessing from what it "sees".

## The problem
When an image is shown to an AI model visually:
- transparency gets flattened, so a transparent PNG looks like it has a white or black background
- fake "transparent" PNGs, with the grey-white checkerboard baked in, fool it
- exact size, DPI, true file format and EXIF/GPS metadata are invisible
- downscaled previews hide blur

## What it detects
| Check | Output |
|---|---|
| Transparency | REAL / NOT / FAKE checkerboard / alpha unused, % transparent, subject bounding box |
| True format | real format vs file extension (catches a PNG renamed to .jpg) |
| Dimensions | size, megapixels, aspect ratio, DPI, print size at 300 DPI |
| Colors | dominant colors as hex + %, likely background color, grayscale check |
| Quality | sharpness score + "likely blurry" hint, blank/solid image warning |
| Animation | frame count and frame duration (GIF/WebP) |
| Metadata | camera, software, date, **GPS location warning** |
| Previews | image composited on magenta and black, so the real cutout is visible |

## Install
**Claude app:** download this repo as a ZIP and upload it under *Settings → Capabilities → Skills*.
**Claude Code:** copy the folder into `~/.claude/skills/image-recognition/`.

## Use with other AI tools
`SKILL.md` follows the open **Agent Skills** standard, so this skill is not Claude-only.

First get the skill folder:
```bash
git clone https://github.com/i-smiling-buddha/transparent-png-check image-recognition
```

**OpenAI Codex CLI**
```bash
# for all your projects
mkdir -p ~/.agents/skills && cp -r image-recognition ~/.agents/skills/
# or only for one repo
mkdir -p .agents/skills && cp -r image-recognition .agents/skills/
```

**Other Agent Skills–compatible tools** (Cursor, GitHub Copilot, Gemini CLI and more): copy the folder into the tool's skills directory. Check that tool's docs for the exact path, because each tool picks its own.

**ChatGPT / Gemini chat apps** (no skill system):
1. Paste the contents of `SKILL.md` into a Custom GPT / Gem's instructions, or at the start of a chat.
2. Upload `scripts/inspect_image.py` together with your image, and ask the AI to run it. This needs code execution turned on (e.g. ChatGPT's data analysis).

**AI tools without code execution:** the skill can't run there. Run the script yourself (below) and paste the output into the chat instead.

## Use the script directly
```bash
pip install pillow numpy   # numpy is optional
python3 scripts/inspect_image.py mascot.png logo.jpg --out previews
python3 scripts/inspect_image.py mascot.png --json
```

## License
MIT. Made by **Smiling Buddha** · Chandoriya Technology
