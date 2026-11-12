# Launch kit

Use this as a starting point for community announcements. Adapt each post to the community rules, disclose that you are the author, and do not cross-post identical text everywhere. Never ask for fake stars, votes, or engagement.

## One-line positioning

**Stop guessing what's in your image. Inspect the actual file.**

A free, MIT-licensed Agent Skill that lets compatible AI agents verify image properties locally with Python: real transparency, true file format, dimensions/DPI, dominant colors, sharpness hints, animation, and EXIF/GPS metadata.

## Short description

AI Image Recognition Skill gives AI coding agents a local Python inspector for image facts that are easy to miss in a chat preview. It can detect likely fake checkerboard transparency, compare actual format with the extension, report dimensions and print estimates, extract dominant colors, inspect animation, and warn when GPS metadata is present.

## X / Twitter

I built an open-source Agent Skill to solve a small but annoying problem: AI can describe an image, but it can still guess wrong about the actual file.

It checks real transparency vs. fake checkerboards, file format, dimensions/DPI, colors, blur hints, animation & EXIF/GPS metadata using local Python.

Free + MIT: https://github.com/i-smiling-buddha/ai-image-recognition-skill

Install: `npx skills add i-smiling-buddha/ai-image-recognition-skill`

## Reddit (show-and-tell)

**Title:** I made a free Agent Skill that checks an image's actual file properties instead of guessing from the preview

**Body:**

I built this because image previews can hide important details. A checkerboard may be baked into a PNG instead of being real transparency; the extension may not match the actual format; and photos can contain GPS metadata you may not want to share.

This open-source Agent Skill runs a small local Python/Pillow inspector and reports:
- Real alpha transparency vs. likely checkerboard pixels
- Detected format vs. filename extension
- Dimensions, aspect ratio, DPI and estimated 300-DPI print size
- Dominant colors, grayscale and likely blur/solid-image hints
- Animation frame count/timing
- EXIF details and a warning when GPS metadata is present
- Magenta/black previews to make transparency visible

It is MIT-licensed and can also be run as a standalone Python script without an agent.

GitHub: https://github.com/i-smiling-buddha/ai-image-recognition-skill

I'd especially appreciate feedback on edge cases and image formats to test. I'm the author.

## Hacker News — Show HN

**Title:** Show HN: AI Image Recognition Skill – inspect image files, not just previews

**Body:**

I built a small open-source Agent Skill that helps compatible coding agents inspect image files using Python/Pillow rather than relying only on a visual preview.

It checks transparency (including likely checkerboards baked into pixels), actual format vs. extension, dimensions, DPI/print estimates, dominant colors, heuristic sharpness, animation, and EXIF/GPS metadata. It also generates magenta and black composites for transparency review.

The inspector can be used independently of an agent, and the project is MIT-licensed.

Code and install instructions: https://github.com/i-smiling-buddha/ai-image-recognition-skill

Feedback and test cases are welcome.

## Dev.to article outline

**Suggested title:** Your AI Can See the Image. Can It Inspect the File?

1. The gap between visual understanding and file-level facts
2. Why fake transparency and extension mismatches matter
3. What the inspector checks
4. A quick install with `npx skills add`
5. Running the Python script directly
6. Privacy: why EXIF/GPS metadata matters
7. Limitations: heuristics are not guarantees
8. Invite readers to test edge cases and contribute

Include a real example image and terminal output only after testing them yourself. Do not invent benchmark results.

## Marketplace submission checklist

- [ ] Confirm the public repository URL and default branch.
- [ ] Verify the skill installs with the current Skills CLI.
- [ ] Confirm the `SKILL.md` name and description are accurate.
- [ ] Test at least PNG with alpha, opaque PNG, JPEG, WebP, and an animated image.
- [ ] Check the README links and banner image render.
- [ ] Submit the repository to relevant skill directories using their current submission flow.
- [ ] If a directory requires Google/GitHub OAuth and it fails, use its documented manual submission or support channel if available; do not share tokens or create duplicate accounts to bypass auth.

## First-week distribution plan

**Day 1:** Publish the improved README, test install, create a release, and add a short demo showing real vs. fake transparency.

**Day 2:** Submit to relevant Agent Skills directories and verify each listing.

**Day 3:** Publish one tailored Reddit post in the most relevant community, following its self-promotion rules.

**Day 4:** Post the short X thread with a real screenshot or short screen recording.

**Day 5:** Publish Show HN only when the demo and install path are verified.

**Day 6:** Publish the Dev.to tutorial with actual commands and outputs.

**Day 7:** Respond to feedback, open issues for confirmed bugs, and ship a small follow-up release if warranted.

## Assets

| Asset | File |
|---|---|
| Fake vs real transparency (real inspector previews) | `docs/assets/fake-vs-real-transparency.png` — the best first image for any post |
| Terminal demo GIF (real `inspect_image.py` output) | `docs/assets/inspector-demo.gif` |
| Social preview (1280×660, < 1 MB) | `ai-image-recognition-banner.jpg` → upload in *Settings → General → Social preview* |

## LinkedIn

Ever downloaded a "transparent PNG" and found a checkerboard baked into the pixels? AI chat
previews can't always tell either.

I've open-sourced **AI Image Recognition Skill** — a free Agent Skill that lets your AI agent
inspect the actual image file: real vs fake transparency, true format, size/DPI for print, dominant
colors, blur hints, animation, and GPS metadata you may not want to share.

Works with Claude Code, Codex, Cursor and more:
`npx skills add i-smiling-buddha/ai-image-recognition-skill`

Free and MIT 👉 https://github.com/i-smiling-buddha/ai-image-recognition-skill

#OpenSource #AI #Design #DeveloperTools

## हिंदी post (X / LinkedIn / WhatsApp)

"Transparent PNG" download किया और बाद में पता चला कि checkerboard तो image में ही छपा हुआ है? 😅
AI भी अक्सर preview देखकर यही गलती करता है।

मैंने एक free, open-source skill बनाई है — **AI Image Recognition Skill**। यह असली file check करती है:
- transparency असली है या नकली checkerboard
- file का असली format, size और print के लिए DPI
- main colors के hex codes, blur, animation
- photo में GPS location तो नहीं छुपी

Install: `npx skills add i-smiling-buddha/ai-image-recognition-skill`
GitHub: https://github.com/i-smiling-buddha/ai-image-recognition-skill (हिंदी गाइड भी है)

## YouTube Shorts / Reels script (faceless, 30 s, Hindi voiceover)

1. **Hook (0–3 s)** — screen: the fake checkerboard PNG on a website, looking broken. VO: "Transparent PNG लगाया, website पर checkerboard आ गया?"
2. **Reveal (3–15 s)** — screen: `docs/assets/fake-vs-real-transparency.png`. VO: "क्योंकि ये transparency नकली थी — checkerboard pixels में ही बना हुआ है।"
3. **Demo (15–25 s)** — screen: `docs/assets/inspector-demo.gif`. VO: "ये free skill आपके AI agent को असली file check करना सिखाती है — FAKE या REAL, सेकंडों में।"
4. **CTA (25–30 s)** — screen: install command + GitHub URL. VO: "एक command, बिल्कुल free। Link description में।"

## Repository metadata

- **Description:** `Free Agent Skill: your AI checks the real image file — fake vs real transparency, true format, size/DPI, colors, blur, animation, GPS metadata. Claude Code, Codex, Cursor.`
- **Website:** `https://desitechnology.com`
- **Topics:** `ai-agents`, `agent-skills`, `claude-code`, `codex`, `cursor`, `image-processing`, `image-analysis`, `transparency`, `png`, `exif`, `metadata`, `privacy`, `pillow`, `python`, `design-tools`, `vibe-coding`, `developer-tools`

## Good first issues (ideas)

1. Detect fake transparency on JPEGs saved from checkerboard previews (lossy edges).
2. Add AVIF / HEIC support notes and tests.
3. Report color profile (sRGB vs Display P3) more clearly.
4. Hindi output mode for the human-readable report.
5. Sample images folder with expected outputs for regression tests.

## Cross-promotion

End posts with: "Also from me: **Smart Model Router** — routes each coding task to the cheapest model that can do it: https://github.com/i-smiling-buddha/smart-model-router-skill"

## Success metrics

Track weekly GitHub stars, forks, unique visitors, clone counts (if available), issues, pull requests, and successful installs where a directory exposes install data. Do not treat stars alone as proof of adoption.
