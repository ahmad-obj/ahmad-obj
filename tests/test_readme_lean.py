from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LeanReadmeTests(unittest.TestCase):
    def test_only_name_svg_remains(self):
        svgs = sorted(
            path.relative_to(ROOT).as_posix()
            for path in ROOT.rglob("*.svg")
            if ".git" not in path.parts
        )
        self.assertEqual(svgs, ["assets/editorial/00-cover.svg"])

    def test_readme_has_one_image_and_no_generated_media(self):
        text = (ROOT / "README.md").read_text()
        self.assertEqual(text.count("<img "), 1)
        self.assertIn("assets/editorial/00-cover.svg", text)
        for bad in [".gif", ".png", "assets/motion/", "assets/typography/"]:
            self.assertNotIn(bad, text)

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


if __name__ == "__main__":
    unittest.main()
