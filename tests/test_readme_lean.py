from pathlib import Path
import unittest
from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parents[1]


class LeanReadmeTests(unittest.TestCase):
    def test_readme_is_text_first_with_only_one_large_svg(self):
        text = (ROOT / "README.md").read_text()
        self.assertEqual(text.count("assets/editorial/00-cover.svg"), 1)
        for old in [
            "01-automotive.svg", "02-orchestration.svg", "03-digit.svg",
            "04-secondary.svg", "05-stack.svg", "06-end.svg"
        ]:
            self.assertNotIn(old, text)
        self.assertNotIn("raw.githubusercontent.com/ahmad-obj/3dcarweb", text)
        for gif in ["ascii-interference.gif", "selected-work.gif"]:
            self.assertIn(f"./assets/motion/{gif}", text)

    def test_readme_contains_real_project_text_and_links(self):
        text = (ROOT / "README.md").read_text()
        expected = [
            ("3D Automotive Experience", "https://github.com/ahmad-obj/3dcarweb"),
            ("Multimodel Orchestration", "https://github.com/ahmad-obj/multimodel-orchestration"),
            ("AI Digit Recognizer", "https://github.com/ahmad-obj/AI-digit-recognizer"),
            ("Sixty-Four", "https://github.com/ahmad-obj/Chess"),
        ]
        for title, url in expected:
            self.assertIn(title, text)
            self.assertIn(url, text)
        for bad in [
            "status: building", "current_mode", "builder / creator",
            "github-readme-stats", "shields.io"
        ]:
            self.assertNotIn(bad, text)

    def test_motion_assets_are_narrow_fast_looping_and_small(self):
        specs = {
            "ascii-interference.gif": (1000, 110),
            "selected-work.gif": (1000, 126),
        }
        for name, size in specs.items():
            p = ROOT / "assets" / "motion" / name
            self.assertTrue(p.exists(), name)
            self.assertLess(p.stat().st_size, 1_000_000, name)
            with Image.open(p) as im:
                self.assertEqual(im.size, size)
                self.assertEqual(im.info.get("loop"), 0)
                self.assertGreaterEqual(im.n_frames, 96)
                durations = []
                for i in range(min(im.n_frames, 12)):
                    im.seek(i)
                    durations.append(im.info.get("duration", 0))
                self.assertTrue(all(30 <= d <= 50 for d in durations), durations)

    def test_motion_loops_do_not_jump_at_the_seam(self):
        for name in ["ascii-interference.gif", "selected-work.gif"]:
            p = ROOT / "assets" / "motion" / name
            with Image.open(p) as im:
                im.seek(0)
                first = im.convert("RGB")
                im.seek(im.n_frames - 1)
                last = im.convert("RGB")
            stat = ImageStat.Stat(ImageChops.difference(first, last))
            mean = sum(stat.mean) / 3
            self.assertLess(mean, 1.0, (name, mean))


if __name__ == "__main__":
    unittest.main()
