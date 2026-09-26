from pathlib import Path
import unittest

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
TYPO = ROOT / "assets" / "typography"


class ReadmeTypographyTests(unittest.TestCase):
    ASSETS = {
        "current.png": (1000, range(100, 151)),
        "academic.png": (1000, range(100, 151)),
        "interests.png": (1000, range(100, 151)),
    }

    def _assert_asset(self, name: str) -> None:
        path = TYPO / name
        self.assertTrue(path.exists(), f"missing {path}")
        self.assertLess(path.stat().st_size, 150_000, name)
        with Image.open(path) as im:
            self.assertEqual(im.width, 1000, name)
            self.assertIn(im.height, self.ASSETS[name][1], name)
            self.assertEqual(im.mode, "RGB", name)

    def test_current_asset(self):
        self._assert_asset("current.png")

    def test_academic_asset(self):
        self._assert_asset("academic.png")

    def test_interests_asset(self):
        self._assert_asset("interests.png")

    def test_typography_assets_stay_lightweight(self):
        paths = [TYPO / name for name in self.ASSETS]
        for path in paths:
            self.assertTrue(path.exists(), f"missing {path}")
        self.assertLess(sum(path.stat().st_size for path in paths), 450_000)

    def test_readme_v3_structure_and_fallback_text(self):
        text = (ROOT / "README.md").read_text()
        tokens = [
            "./assets/editorial/00-cover.svg",
            "./assets/typography/current.png",
            "### Current",
            "./assets/typography/academic.png",
            "### Academic",
            "./assets/typography/interests.png",
            "### Interests",
            "./assets/motion/ascii-interference.gif",
            "./assets/motion/selected-work.gif",
            "3D Automotive Experience",
            "### Other work",
            "### Tools",
        ]
        positions = []
        for token in tokens:
            self.assertIn(token, text, token)
            positions.append(text.index(token))
        self.assertEqual(positions, sorted(positions))

        for phrase in [
            "Real-time graphics",
            "Agent orchestration",
            "Experimental interfaces",
            "BS Computer Science — FAST-NUCES",
            "Dean’s List ×2",
            "1st position — BISE Gujranwala ICS",
            "AI systems",
            "Developer tooling",
            "Interaction design",
            "Systems programming",
        ]:
            self.assertIn(phrase, text)

    def test_readme_remains_text_first(self):
        text = (ROOT / "README.md").read_text()
        for banned in [
            "01-automotive.svg",
            "02-orchestration.svg",
            "03-digit.svg",
            "04-secondary.svg",
            "05-stack.svg",
            "06-end.svg",
            "raw.githubusercontent.com/ahmad-obj/3dcarweb",
            "github-readme-stats",
            "shields.io",
            "status: building",
            "current_mode",
        ]:
            self.assertNotIn(banned, text)

        first_project = text.index("3D Automotive Experience")
        visual_refs_before_projects = text[:first_project].count("<img ")
        self.assertLessEqual(visual_refs_before_projects, 5)


if __name__ == "__main__":
    unittest.main()
