from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

class ReadmeTextArtTests(unittest.TestCase):
    def test_ahmad_cover_is_the_only_image_asset(self):
        image_exts = {".svg", ".png", ".gif", ".webp", ".jpg", ".jpeg"}
        images = sorted(
            p.relative_to(ROOT).as_posix()
            for p in ROOT.rglob("*")
            if p.is_file() and p.suffix.lower() in image_exts and ".git" not in p.parts
        )
        self.assertEqual(images, ["assets/editorial/00-cover.svg"])

    def test_readme_uses_only_the_ahmad_image(self):
        text = README.read_text()
        self.assertEqual(text.count("<img "), 1)
        self.assertIn("./assets/editorial/00-cover.svg", text)
        for banned in [".png", ".gif", "assets/motion/", "assets/typography/"]:
            self.assertNotIn(banned, text)

    def test_readme_contains_designed_text_art_sections(self):
        text = README.read_text()
        for marker in [
            "CURRENT / FLOW",
            "ACADEMIC / ASCENT",
            "INTERESTS / CONSTELLATION",
            "SELECTED / WORK",
            "░░▒▒▓▓",
            "⣿",
            "⠂",
            "REAL-TIME GRAPHICS",
            "AGENT ORCHESTRATION",
            "EXPERIMENTAL INTERFACES",
        ]:
            self.assertIn(marker, text)

    def test_text_art_stays_mobile_reasonable(self):
        text = README.read_text()
        in_fence = False
        for line in text.splitlines():
            if line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                self.assertLessEqual(len(line), 72, line)

    def test_profile_content_remains_native_text(self):
        text = README.read_text()
        for phrase in [
            "BS Computer Science — FAST-NUCES",
            "Dean’s List ×2",
            "1st position — BISE Gujranwala ICS",
            "3D Automotive Experience",
            "Multimodel Orchestration",
            "AI Digit Recognizer",
            "Sixty-Four",
            "WEBERAISE",
            "Scout Email",
        ]:
            self.assertIn(phrase, text)

if __name__ == "__main__":
    unittest.main()
