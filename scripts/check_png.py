import sys, os
from PIL import Image

def checker_score(img, block=8):
    """Fake-transparency detect: corners में gray/white checkerboard pattern है या नहीं."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    hits = 0
    for (cx, cy) in [(0, 0), (w - 4 * block, 0), (0, h - 4 * block), (w - 4 * block, h - 4 * block)]:
        if cx < 0 or cy < 0:
            continue
        vals = []
        for by in range(4):
            for bx in range(4):
                r, g, b = rgb.getpixel((cx + bx * block + block // 2, cy + by * block + block // 2))
                vals.append((r, g, b, (bx + by) % 2))
        grayish = all(abs(r - g) < 12 and abs(g - b) < 12 and r > 150 for r, g, b, _ in vals)
        even = [v[0] for v in vals if v[3] == 0]
        odd = [v[0] for v in vals if v[3] == 1]
        if grayish and abs(sum(even) / len(even) - sum(odd) / len(odd)) > 15:
            hits += 1
    return hits

def analyze(path, out_dir="."):
    img = Image.open(path)
    print(f"File: {path}")
    print(f"Size: {img.width}x{img.height}  Mode: {img.mode}")
    if img.mode == "P" and "transparency" in img.info:
        img = img.convert("RGBA")
    if img.mode in ("LA", "PA"):
        img = img.convert("RGBA")
    if img.mode != "RGBA":
        print("Alpha channel: NAHI — image poori tarah opaque hai.")
        hits = max(checker_score(img, b) for b in (8, 10, 12, 16, 20))
        if hits >= 2:
            print("WARNING: Corners me checkerboard pattern mila — ye FAKE transparent PNG lagta hai (pattern image me baked hai).")
        return
    a = img.getchannel("A")
    hist = a.histogram()
    total = img.width * img.height
    full_t = hist[0]
    full_o = hist[255]
    semi = total - full_t - full_o
    print(f"Alpha channel: HAI")
    print(f"Fully transparent: {full_t / total:.1%}  Semi-transparent: {semi / total:.1%}  Opaque: {full_o / total:.1%}")
    print(f"Subject bounding box (alpha>0): {a.getbbox()}")
    if full_t == 0 and semi == 0:
        print("NOTE: Alpha channel hai lekin har pixel opaque hai — effectively background maujood hai.")
    base = os.path.splitext(os.path.basename(path))[0]
    for name, color in [("magenta", (255, 0, 255, 255)), ("black", (0, 0, 0, 255))]:
        bg = Image.new("RGBA", img.size, color)
        bg.alpha_composite(img)
        p = os.path.join(out_dir, f"{base}_on_{name}.png")
        bg.convert("RGB").save(p)
        print(f"Preview: {p}")

if __name__ == "__main__":
    for p in sys.argv[1:]:
        analyze(p)
        print()
