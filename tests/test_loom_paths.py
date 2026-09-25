import unittest

from tools.loom.config import LoomConfig
from tools.loom.model import GridState
from tools.loom.paths import (
    OPPOSITE,
    Route,
    RouteSegment,
    assign_crossings,
    classify_routes,
    select_signature_routes,
    trace_routes,
)


class LoomPathTests(unittest.TestCase):
    def test_all_tile_arcs_are_consumed_once(self):
        grid = GridState(3, 2, ((0, 1, 0), (1, 0, 1)), {})
        routes = trace_routes(grid)
        self.assertEqual(sum(len(route.segments) for route in routes), 3 * 2 * 2)
        seen = {(s.x, s.y, frozenset((s.entry, s.exit))) for r in routes for s in r.segments}
        self.assertEqual(len(seen), 12)

    def test_route_segments_are_edge_continuous(self):
        grid = GridState(4, 3, ((0, 1, 1, 0), (1, 0, 1, 0), (0, 0, 1, 1)), {})
        for route in trace_routes(grid):
            for a, b in zip(route.segments, route.segments[1:]):
                dx, dy = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}[a.exit]
                self.assertEqual((a.x + dx, a.y + dy, OPPOSITE[a.exit]), (b.x, b.y, b.entry))

    def test_open_route_endpoints_are_on_outer_boundary(self):
        grid = GridState(2, 2, ((0, 0), (0, 0)), {})
        routes = trace_routes(grid)
        for route in routes:
            if route.closed:
                continue
            first, last = route.segments[0], route.segments[-1]
            self.assertTrue(self._is_boundary(first, first.entry, grid))
            self.assertTrue(self._is_boundary(last, last.exit, grid))

    def test_closed_loop_returns_to_its_start_half_edge(self):
        grid = GridState(2, 2, ((1, 0), (0, 1)), {})
        closed = [r for r in trace_routes(grid) if r.closed]
        self.assertTrue(closed)
        for route in closed:
            first, last = route.segments[0], route.segments[-1]
            dx, dy = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}[last.exit]
            self.assertEqual((last.x + dx, last.y + dy, OPPOSITE[last.exit]), (first.x, first.y, first.entry))

    def test_degenerate_empty_grid_is_valid(self):
        self.assertEqual(trace_routes(GridState(0, 0, tuple(), {})), [])

    def test_exact_hierarchy_boundaries(self):
        cfg = LoomConfig()
        routes = [self._route(i, n) for i, n in enumerate((1, 4, 5, 10, 11, 18, 19, 30))]
        classified = classify_routes(routes, cfg)
        self.assertEqual([r.tier for r in classified], [
            "whisper", "whisper", "resident", "resident", "major", "major", "signature", "signature"
        ])

    def test_signature_selection_never_exceeds_three(self):
        cfg = LoomConfig()
        routes = classify_routes([self._route(i, 19 + i) for i in range(7)], cfg)
        selected = select_signature_routes(routes, limit=3)
        self.assertEqual(len(selected), 3)
        self.assertTrue(all(r.tier == "signature" for r in selected))

    def test_crossing_ownership_prefers_higher_tier(self):
        low = Route(1, (RouteSegment(5, 5, "N", "E"),), False, "resident")
        high = Route(2, tuple(RouteSegment(5, 5, "S", "W") for _ in range(20)), False, "signature")
        crossings = assign_crossings([low, high])
        self.assertTrue(crossings)
        self.assertEqual(crossings[0].upper_route_id, 2)
        self.assertEqual(crossings[0].lower_route_id, 1)

    @staticmethod
    def _is_boundary(seg, side, grid):
        return (
            (side == "N" and seg.y == 0)
            or (side == "S" and seg.y == grid.rows - 1)
            or (side == "W" and seg.x == 0)
            or (side == "E" and seg.x == grid.cols - 1)
        )

    @staticmethod
    def _route(route_id, length):
        segs = tuple(RouteSegment(i % 30, (i // 30) % 11, "N", "E") for i in range(length))
        return Route(route_id, segs, False)


if __name__ == "__main__":
    unittest.main()
