import unittest
from collections import Counter

from tools.loom.config import LoomConfig
from tools.loom.model import build_cycle, build_initial_grid, state_at


class LoomModelTests(unittest.TestCase):
    def test_initial_grid_shape_values_and_determinism(self):
        cfg = LoomConfig()
        a = build_initial_grid(cfg)
        b = build_initial_grid(cfg)
        self.assertEqual((a.cols, a.rows), (30, 11))
        self.assertEqual(a.cells, b.cells)
        self.assertEqual(len(a.cells), 11)
        self.assertTrue(all(len(row) == 30 for row in a.cells))
        self.assertTrue({value for row in a.cells for value in row} <= {0, 1})

    def test_seed_changes_initial_grid_or_schedule(self):
        a_cfg = LoomConfig(seed=20260925)
        b_cfg = LoomConfig(seed=20260926)
        a_grid = build_initial_grid(a_cfg)
        b_grid = build_initial_grid(b_cfg)
        a_events = build_cycle(a_cfg, a_grid)
        b_events = build_cycle(b_cfg, b_grid)
        self.assertTrue(a_grid.cells != b_grid.cells or a_events != b_events)

    def test_cycle_returns_to_initial_state(self):
        cfg = LoomConfig()
        initial = build_initial_grid(cfg)
        events = build_cycle(cfg, initial)
        self.assertEqual(state_at(cfg, initial, events, 0.0), state_at(cfg, initial, events, 18.0))

    def test_every_scheduled_cell_flips_even_number_of_times(self):
        cfg = LoomConfig()
        initial = build_initial_grid(cfg)
        events = build_cycle(cfg, initial)
        counts = Counter(cell for event in events for cell in event.cells)
        self.assertTrue(counts)
        self.assertTrue(all(count % 2 == 0 for count in counts.values()))
        self.assertTrue(all(1 <= len(event.cells) <= 6 for event in events))

    def test_exactly_three_growth_zones_are_used(self):
        cfg = LoomConfig()
        initial = build_initial_grid(cfg)
        events = build_cycle(cfg, initial)
        self.assertEqual({event.zone for event in events}, {"primary", "secondary", "repair"})

    def test_state_exposes_transition_progress_during_flip(self):
        cfg = LoomConfig()
        initial = build_initial_grid(cfg)
        events = build_cycle(cfg, initial)
        event = events[0]
        mid = state_at(cfg, initial, events, event.time + cfg.transition_s / 2)
        self.assertTrue(mid.transitions)
        for progress in mid.transitions.values():
            self.assertGreater(progress, 0.0)
            self.assertLess(progress, 1.0)


if __name__ == "__main__":
    unittest.main()
