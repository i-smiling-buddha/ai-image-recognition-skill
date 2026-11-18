import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_image.py"


def checkerboard_subject(size=240, tile=8, light=255, dark=204):
    """A grey/white checkerboard with an opaque subject in the middle, leaving
    all four corners showing the checkerboard — i.e. fake (baked-in) transparency."""
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            px[x, y] = (light,) * 3 if ((x // tile) + (y // tile)) % 2 == 0 else (dark,) * 3
    ImageDraw.Draw(img).ellipse(
        [size * 0.30, size * 0.30, size * 0.70, size * 0.70], fill=(40, 120, 200)
    )
    return img


class CheckerJpegTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def verdict(self, path):
        output = subprocess.check_output(
            [sys.executable, str(SCRIPT), str(path), "--out", str(self.root / "previews"), "--json"],
            text=True,
        )
        report, = json.loads(output)
        return report["transparency_verdict"]

    def test_near_white_checkerboard_detected_in_jpeg(self):
        # A faint near-white/near-grey checkerboard (contrast ~16) that JPEG
        # compression would otherwise soften below the crisp-image thresholds.
        path = self.root / "fake_transparency.jpg"
        checkerboard_subject(tile=8, light=248, dark=232).save(path, "JPEG", quality=65)
        self.assertIn("FAKE transparency", self.verdict(path))

    def test_crisp_png_checkerboard_still_detected(self):
        # Regression guard: the relaxed JPEG path must not weaken PNG detection.
        path = self.root / "fake_transparency.png"
        checkerboard_subject(tile=8, light=255, dark=204).save(path)
        self.assertIn("FAKE transparency", self.verdict(path))

    def test_solid_background_jpeg_not_flagged(self):
        # False-positive guard: an ordinary opaque subject on a solid background
        # must not be mistaken for a baked checkerboard.
        img = Image.new("RGB", (240, 240), (255, 255, 255))
        ImageDraw.Draw(img).ellipse([60, 60, 180, 180], fill=(200, 60, 60))
        path = self.root / "solid_background.jpg"
        img.save(path, "JPEG", quality=70)
        self.assertNotIn("FAKE transparency", self.verdict(path))


if __name__ == "__main__":
    unittest.main()
