import tempfile
import unittest
from pathlib import Path

from PIL import Image

from tools.loom.config import LoomConfig
from tools.loom.export import export_delivery_assets


class LoomDeliveryTests(unittest.TestCase):
    def test_delivery_profiles_are_smaller_and_smoother_than_source_gif(self):
        cfg = LoomConfig()
        with tempfile.TemporaryDirectory() as td:
            webp = Path(td) / "loom.webp"
            gif = Path(td) / "loom.gif"
            results = export_delivery_assets(
                cfg,
                webp_path=webp,
                gif_path=gif,
                duration_s=1.0,
                webp_fps=16,
                gif_fps=10,
                width=420,
                gif_width=360,
            )

            self.assertEqual(results["webp"].frame_count, 16)
            self.assertEqual(results["gif"].frame_count, 10)

            with Image.open(webp) as image:
                self.assertTrue(image.is_animated)
                self.assertEqual(image.n_frames, 16)
                self.assertEqual(image.size, (420, 150))
                self.assertEqual(image.info.get("loop"), 0)

            with Image.open(gif) as image:
                self.assertTrue(image.is_animated)
                self.assertEqual(image.n_frames, 10)
                self.assertEqual(image.size, (360, 129))
                self.assertEqual(image.info.get("loop"), 0)

            self.assertLess(results["webp"].size_bytes, results["gif"].size_bytes)

    def test_production_delivery_profile_targets_readme_scale(self):
        cfg = LoomConfig()
        self.assertEqual(cfg.delivery_width, 800)
        self.assertEqual(cfg.delivery_height, 287)
        self.assertEqual(cfg.webp_fps, 15)
        self.assertEqual(cfg.gif_fps, 6)
        self.assertEqual(cfg.gif_width, 720)
        self.assertEqual(cfg.gif_height, 258)


if __name__ == "__main__":
    unittest.main()
