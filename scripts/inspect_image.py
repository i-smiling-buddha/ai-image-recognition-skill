"""
inspect_image.py — facts about an image from its pixels and file data, not from vision.

Usage: python3 inspect_image.py <image> [more images ...] [--out DIR] [--json]
Requires: Pillow (pip install pillow). numpy is optional (faster, adds blur score).
"""
import sys, os, json
from PIL import Image, ImageOps, ExifTags

try:
    import numpy as np
except ImportError:
    np = None

def pixels(im):
    """Pixel list that works on old and new Pillow (getdata is deprecated in Pillow 12+)."""
    f = getattr(im, "get_flattened_data", None)
    return list(f()) if f else list(im.getdata())

def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

def ratio(w, h):
    from math import gcd
    g = gcd(w, h)
    r = f"{w//g}:{h//g}"
    common = {"1:1": "square", "16:9": "widescreen", "9:16": "vertical/story", "4:3": "", "3:4": "", "3:2": "", "2:3": ""}
    return r + (f" ({common[r]})" if common.get(r) else "") if (w//g) < 50 else f"{w/h:.3f}"

def checker_score(img):
    """Fake transparency: grey/white checkerboard baked into the corners."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    best = 0
    for block in (8, 10, 12, 16, 20):
        hits = 0
        for cx, cy in [(0, 0), (w - 4*block, 0), (0, h - 4*block), (w - 4*block, h - 4*block)]:
            if cx < 0 or cy < 0:
                continue
            vals = []
            for by in range(4):
                for bx in range(4):
                    r, g, b = rgb.getpixel((cx + bx*block + block//2, cy + by*block + block//2))
                    vals.append((r, g, b, (bx + by) % 2))
            grey = all(abs(r-g) < 12 and abs(g-b) < 12 and r > 150 for r, g, b, _ in vals)
            even = [v[0] for v in vals if v[3] == 0]
            odd = [v[0] for v in vals if v[3] == 1]
            if grey and abs(sum(even)/len(even) - sum(odd)/len(odd)) > 15:
                hits += 1
        best = max(best, hits)
    return best

def dominant_colors(img, k=5):
    rgba = img.convert("RGBA")
    rgba.thumbnail((200, 200))
    px = [p[:3] for p in pixels(rgba) if p[3] > 128]
    if not px:
        return []
    small = Image.new("RGB", (len(px), 1))
    small.putdata(px)
    q = small.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)
    total = sum(c for c, _ in counts)
    return [(f"#{pal[i*3]:02x}{pal[i*3+1]:02x}{pal[i*3+2]:02x}", round(100*c/total, 1)) for c, i in counts]

def edge_bg_color(img):
    """Most common colour along the border — the likely background if opaque."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    pts = [(x, 0) for x in range(0, w, max(1, w//50))] + [(x, h-1) for x in range(0, w, max(1, w//50))] \
        + [(0, y) for y in range(0, h, max(1, h//50))] + [(w-1, y) for y in range(0, h, max(1, h//50))]
    cols = [rgb.getpixel(p) for p in pts]
    base = max(set(cols), key=cols.count)
    close = sum(1 for c in cols if sum(abs(a-b) for a, b in zip(c, base)) < 30)
    return f"#{base[0]:02x}{base[1]:02x}{base[2]:02x}", round(100*close/len(cols))

def blur_score(img):
    if np is None:
        return None
    g = np.asarray(img.convert("L").resize((min(img.width, 800), max(1, int(min(img.width, 800) * img.height / img.width)))), dtype=float)
    lap = g[1:-1, 1:-1]*4 - g[:-2, 1:-1] - g[2:, 1:-1] - g[1:-1, :-2] - g[1:-1, 2:]
    return round(float(lap.var()), 1)

def exif_summary(img):
    out = {}
    try:
        ex = img.getexif()
    except Exception:
        return out
    if not ex:
        return out
    names = {v: k for k, v in ExifTags.TAGS.items()}
    for key in ("Make", "Model", "Software", "DateTime", "Orientation"):
        tag = names.get(key)
        if tag in ex:
            out[key] = str(ex[tag])
    if 0x8825 in ex:  # GPSInfo
        out["GPS"] = "PRESENT (location embedded — strip before sharing publicly)"
    return out

def analyze(path, out_dir):
    r = {"file": path}
    r["file_size"] = human_size(os.path.getsize(path))
    img = Image.open(path)
    r["format"] = img.format
    r["true_type_matches_extension"] = (
        os.path.splitext(path)[1].lower().lstrip(".").replace("jpg", "jpeg") == (img.format or "").lower()
    )
    r["mode"] = img.mode
    r["size"] = f"{img.width}x{img.height}"
    r["megapixels"] = round(img.width * img.height / 1e6, 2)
    r["aspect_ratio"] = ratio(img.width, img.height)
    dpi = img.info.get("dpi")
    if dpi:
        r["dpi"] = f"{round(dpi[0])}x{round(dpi[1])}"
        r["print_size_inches_at_300dpi"] = f"{img.width/300:.2f} x {img.height/300:.2f}"
    r["icc_profile"] = "yes" if img.info.get("icc_profile") else "no"
    n_frames = getattr(img, "n_frames", 1)
    r["frames"] = n_frames
    if n_frames > 1:
        r["animated"] = True
        r["frame_duration_ms"] = img.info.get("duration")

    ex = exif_summary(img)
    if ex:
        r["exif"] = ex
    img = ImageOps.exif_transpose(img)

    # --- transparency ---
    work = img
    if work.mode == "P" and "transparency" in work.info:
        work = work.convert("RGBA")
    if work.mode in ("LA", "PA"):
        work = work.convert("RGBA")
    if work.mode == "RGBA":
        a = work.getchannel("A")
        hist = a.histogram()
        total = work.width * work.height
        t, o = hist[0], hist[255]
        r["transparency"] = {
            "has_alpha": True,
            "fully_transparent_pct": round(100*t/total, 1),
            "semi_transparent_pct": round(100*(total-t-o)/total, 1),
            "opaque_pct": round(100*o/total, 1),
            "subject_bbox": a.getbbox(),
        }
        if t == 0 and o == total:
            r["transparency"]["note"] = "alpha channel exists but every pixel is opaque - background is still there"
        verdict = "REAL transparency" if t > 0 else "NOT transparent (alpha unused)"
    else:
        r["transparency"] = {"has_alpha": False}
        verdict = "NOT transparent"
        if checker_score(img) >= 2:
            verdict = "FAKE transparency (checkerboard baked into pixels)"
        bg, pct = edge_bg_color(img)
        r["edge_background"] = {"color": bg, "border_match_pct": pct}
    r["transparency_verdict"] = verdict

    # --- content ---
    stat_img = img.convert("RGB")
    ext = stat_img.getextrema()
    r["is_blank_or_solid"] = all(hi - lo < 8 for lo, hi in ext)
    gray = all(
        abs(a - b) < 6 and abs(b - c) < 6
        for a, b, c in pixels(stat_img.resize((64, 64)))
    )
    r["is_grayscale"] = gray
    r["dominant_colors"] = dominant_colors(img)
    b = None if r["is_blank_or_solid"] else blur_score(img)
    if b is not None:
        r["sharpness_score"] = b
        r["sharpness_hint"] = "likely blurry/soft" if b < 60 else ("ok" if b < 300 else "sharp/detailed")

    # --- previews ---
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(path))[0]
    rgba = img.convert("RGBA")
    previews = []
    for name, color in [("magenta", (255, 0, 255, 255)), ("black", (0, 0, 0, 255))]:
        bgimg = Image.new("RGBA", rgba.size, color)
        bgimg.alpha_composite(rgba)
        bgimg.thumbnail((1200, 1200))
        p = os.path.join(out_dir, f"{base}_on_{name}.png")
        bgimg.convert("RGB").save(p)
        previews.append(p)
    r["previews"] = previews
    return r

def print_report(r):
    print(f"=== {r['file']} ===")
    for k, v in r.items():
        if k == "file":
            continue
        if isinstance(v, dict):
            print(f"{k}:")
            for kk, vv in v.items():
                print(f"    {kk}: {vv}")
        elif isinstance(v, list) and k == "dominant_colors":
            print(f"{k}: " + ", ".join(f"{c} ({p}%)" for c, p in v))
        else:
            print(f"{k}: {v}")
    print()

if __name__ == "__main__":
    args = sys.argv[1:]
    as_json = "--json" in args
    out_dir = "."
    if "--out" in args:
        i = args.index("--out")
        out_dir = args[i+1]
        del args[i:i+2]
    files = [a for a in args if a != "--json"]
    if not files:
        print(__doc__)
        sys.exit(1)
    results = []
    for f in files:
        try:
            results.append(analyze(f, out_dir))
        except Exception as e:
            results.append({"file": f, "error": str(e)})
    if as_json:
        print(json.dumps(results, indent=2, default=str))
    else:
        for r in results:
            print_report(r) if "error" not in r else print(f"=== {r['file']} ===\nERROR: {r['error']}\n")
