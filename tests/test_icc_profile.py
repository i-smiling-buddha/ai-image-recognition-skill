import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, features


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "inspect_image.py"


class IccProfileTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.image = Image.new("RGB", (8, 8), "#5879a1")

    def run_inspector(self, path, *args):
        return subprocess.check_output(
            [sys.executable, str(SCRIPT), str(path), "--out", str(self.root / "previews"), *args],
            text=True,
        )

    @unittest.skipUnless(features.check("littlecms2"), "Pillow has no LittleCMS support")
    def test_embedded_description_in_json_and_text(self):
        from PIL import ImageCms

        profile = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
        description = ImageCms.getProfileDescription(profile).strip()
        for extension in ("png", "jpeg", "tiff"):
            with self.subTest(extension=extension):
                path = self.root / f"tagged.{extension}"
                self.image.save(path, icc_profile=profile.tobytes())
                report, = json.loads(self.run_inspector(path, "--json"))
                self.assertEqual(report["icc_profile"], "yes")
                self.assertEqual(report["icc_profile_description"], description)
                self.assertIn(f"icc_profile_description: {description}", self.run_inspector(path))

    def test_missing_profile_preserves_the_presence_flag(self):
        path = self.root / "untagged.png"
        self.image.save(path)
        report, = json.loads(self.run_inspector(path, "--json"))
        self.assertEqual(report["icc_profile"], "no")
        self.assertNotIn("icc_profile_description", report)

    def test_invalid_profile_does_not_break_inspection(self):
        path = self.root / "invalid.png"
        self.image.save(path, icc_profile=b"this is not an ICC profile")
        report, = json.loads(self.run_inspector(path, "--json"))
        self.assertEqual(report["icc_profile"], "yes")
        self.assertNotIn("icc_profile_description", report)
        self.assertEqual(report["size"], "8x8")
