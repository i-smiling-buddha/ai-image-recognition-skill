# AI Image Recognition Skill

![AI Image Recognition Skill banner](ai-image-recognition-banner.jpg)

[![GitHub stars](https://img.shields.io/github/stars/i-smiling-buddha/ai-image-recognition-skill?style=for-the-badge)](https://github.com/i-smiling-buddha/ai-image-recognition-skill/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3-blue.svg?style=for-the-badge)](https://www.python.org/)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills-purple.svg?style=for-the-badge)](https://skills.sh/)
[![skills.sh installs](https://skills.sh/b/i-smiling-buddha/ai-image-recognition-skill)](https://skills.sh/i-smiling-buddha/ai-image-recognition-skill)

**Stop guessing. Inspect the actual image file.**

हिंदी गाइड: **[README.hi.md](README.hi.md)**

AI vision can describe what an image looks like, but it cannot reliably tell you every property hidden in the original file. This open-source Agent Skill gives compatible AI coding agents a local Python image inspector so they can verify transparency, true file format, dimensions, DPI, colors, sharpness hints, animation, and privacy-related metadata using the file itself.

Useful for AI-generated images, design handoffs, transparent PNGs, website assets, app screenshots, print/merch preparation, and product photography.

![Looks transparent? The inspector shows one PNG has a fake checkerboard baked into its pixels and the other has real transparency](docs/assets/fake-vs-real-transparency.png)

## Install

Install with the open Agent Skills CLI:

```bash
npx skills add i-smiling-buddha/ai-image-recognition-skill
```

Choose your target agent when prompted. See the [Skills directory](https://skills.sh/) for the wider ecosystem.

## What it checks

| Check | What you get |
|---|---|
| **Real transparency** | Detects usable alpha transparency, unused alpha channels, and likely checkerboards baked into opaque pixels |
| **True file format** | Compares the image's detected format with its filename extension |
| **Dimensions & print** | Pixel dimensions, megapixels, aspect ratio, embedded DPI, and estimated print dimensions at 300 DPI |
| **Colors** | Dominant colors as hex values, grayscale detection, and likely edge/background color |
| **Image quality** | A heuristic sharpness score and warnings for likely blurry or solid images |
| **Animation** | Frame count and frame timing where available |
| **Metadata & privacy** | Camera/software/date metadata and a warning when GPS metadata is present |
| **Visual previews** | Composites the image over magenta and black so transparent areas are easy to inspect |

## Example tasks

Ask your AI agent:

- “Is this PNG genuinely transparent, or is the checkerboard part of the image?”
- “Check whether this image is large enough for a 300-DPI print.”
- “Find the dominant colors and give me their hex codes.”
- “Does this photo contain GPS metadata I should remove before sharing?”
- “Check whether the file extension matches its real image format.”
- “Is this image animated, and how many frames does it contain?”

The skill combines **programmatic file facts** with visual interpretation. Use the script's report for exact properties and the agent's vision for understanding the depicted content.

## Run the inspector without an AI agent

Requirements: Python 3 and Pillow. NumPy is optional; it adds the sharpness estimate. Use a virtual environment to keep dependencies isolated.

```bash
# Create a virtual environment
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux (use this instead of the Windows command)
source .venv/bin/activate

# Install dependencies
python -m pip install pillow
# Optional: python -m pip install numpy

# Inspect one or more images
python scripts/inspect_image.py path/to/image.png --out previews

# Get machine-readable JSON
python scripts/inspect_image.py path/to/image.png --json
```

![Terminal demo: inspect_image.py reports FAKE transparency for one PNG and REAL transparency for another](docs/assets/inspector-demo.gif)

Replace the example path with your image path. The script reads the supplied image and writes magenta/black preview images to the output directory.

## Compatibility

This repository follows the open [Agent Skills format](https://agentskills.io/). It is designed for compatible agents and tools that can load a `SKILL.md`, run local Python, and access the target image file. The Skills CLI can install it into supported agents; exact support and installation locations vary by tool.

For a chat app without a skill loader, provide `SKILL.md` as the instructions and make sure the agent has code execution plus access to both `scripts/inspect_image.py` and the image file.

## Important limitations

- Checkerboard detection, likely-background detection, and sharpness are **heuristics**, not guarantees. Review the previews and image when the distinction matters.
- A sharpness score is only produced when NumPy is installed and the image is suitable for the calculation.
- Print-size estimates are based on 300 DPI; they do not guarantee print quality.
- Metadata availability depends on the image format and the metadata embedded in the file.
- The inspector does not edit or overwrite the original image. Review generated reports before sharing them.

**Privacy note:** image metadata can reveal where a photo was taken. If GPS metadata is reported, consider removing it before publishing the image.

## More free skills by Smiling Buddha

- **[Smart Model Router Skill](https://github.com/i-smiling-buddha/smart-model-router-skill)** — save tokens and API credits: your agent routes each coding task to the cheapest model that can reliably do it, verifies the result, and escalates only when it fails. `npx skills add i-smiling-buddha/smart-model-router-skill`

## Contributing

Issues, bug reports, test images (with personal metadata removed), and pull requests are welcome. Please avoid uploading private or sensitive images in public issues. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT. Made by [Smiling Buddha](https://github.com/i-smiling-buddha) · [DESITechnology](https://desitechnology.com).
