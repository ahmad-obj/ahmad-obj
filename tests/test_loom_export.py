import hashlib
from dataclasses import replace
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageChops, ImageSequence, ImageStat

from tools.loom.config import LoomConfig
from tools.loom.export import export_animation, render_at
from tools.loom.model import build_cycle, build_initial_grid, state_at


class LoomExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = LoomConfig()
        cls.tmp = tempfile.TemporaryDirectory()
        cls.fast_cfg = replace(cls.cfg, fps=1)
        cls.a = Path(cls.tmp.name) / "a.gif"
        cls.b = Path(cls.tmp.name) / "b.gif"
        cls.poster = Path(cls.tmp.name) / "poster.png"
        cls.result_a = export_animation(cls.fast_cfg, cls.a, cls.poster)
        cls.result_b = export_animation(cls.fast_cfg, cls.b, None)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_exact_frame_count_dimensions_and_infinite_loop(self):
        with Image.open(self.a) as gif:
            frames = list(ImageSequence.Iterator(gif))
            self.assertEqual(gif.n_frames, 18)
            self.assertEqual(gif.size, (1200, 430))
            self.assertEqual(gif.info.get("loop"), 0)
        self.assertEqual(round(self.cfg.duration_s * self.cfg.fps), 216)

    def test_logical_state_closes_at_eighteen_seconds(self):
        initial = build_initial_grid(self.cfg)
        events = build_cycle(self.cfg, initial)
        self.assertEqual(state_at(self.cfg, initial, events, 0.0), state_at(self.cfg, initial, events, 18.0))

    def test_visual_seam_is_quiet(self):
        first = render_at(self.cfg, 0.0)
        last = render_at(self.cfg, self.cfg.duration_s - 1 / self.cfg.fps)
        diff = ImageChops.difference(first, last)
        mean = sum(ImageStat.Stat(diff).mean) / 3
        self.assertLess(mean, 1.5)

    def test_asset_stays_under_hard_size_cap(self):
        self.assertLessEqual(self.result_a.size_bytes, 10 * 1024 * 1024)

    def test_same_seed_exports_identical_bytes(self):
        sha_a = hashlib.sha256(self.a.read_bytes()).hexdigest()
        sha_b = hashlib.sha256(self.b.read_bytes()).hexdigest()
        self.assertEqual(sha_a, sha_b)
        self.assertEqual(sha_a, self.result_a.sha256)

    def test_poster_is_production_size(self):
        with Image.open(self.poster) as poster:
            self.assertEqual(poster.size, (1200, 430))


if __name__ == "__main__":
    unittest.main()
