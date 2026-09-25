import unittest
from statistics import median

from tools.loom.config import LoomConfig
from tools.loom.model import GridState, build_cycle, build_initial_grid, state_at
from tools.loom.paths import Route, RouteSegment, assign_crossings, classify_routes, trace_routes
from tools.loom.render import _lifted_points, _route_points, render_frame


class LoomRenderTests(unittest.TestCase):
    def setUp(self):
        self.cfg = LoomConfig()
        self.state = GridState(self.cfg.cols, self.cfg.rows, tuple(tuple(0 for _ in range(self.cfg.cols)) for _ in range(self.cfg.rows)), {})

    def test_frame_contract_and_vellum_background(self):
        frame = render_frame(self.cfg, self.state, [], [], 0.0)
        self.assertEqual(frame.size, (1200, 430))
        self.assertIn(frame.mode, {"RGB", "RGBA"})
        samples = [frame.getpixel((x, y))[:3] for x, y in ((5, 5), (1194, 5), (5, 424), (1194, 424), (600, 20))]
        med = tuple(int(median(channel)) for channel in zip(*samples))
        self.assertTrue(232 <= med[0] <= 247)
        self.assertTrue(226 <= med[1] <= 243)
        self.assertTrue(214 <= med[2] <= 236)
        self.assertNotIn("text", frame.info)

    def test_graphite_dominates_ultramarine_and_accent_stays_below_eight_percent(self):
        signature = self._horizontal_signature(7, 24)
        resident = Route(4, tuple(RouteSegment(x, 8, "W", "N") for x in range(3, 12)), False, "resident", 900)
        frame = render_frame(self.cfg, self.state, [signature, resident], assign_crossings([signature, resident]), 10.0)
        graphite = accent = routeish = 0
        for r, g, b in frame.getdata():
            d_graphite = abs(r - 25) + abs(g - 26) + abs(b - 28)
            d_accent = abs(r - 45) + abs(g - 79) + abs(b - 184)
            if d_graphite < 75:
                graphite += 1
                routeish += 1
            elif d_accent < 75:
                accent += 1
                routeish += 1
        self.assertGreater(graphite, accent)
        self.assertGreater(routeish, 0)
        self.assertLess(accent / routeish, 0.08)

    def test_signature_route_creates_soft_shadow(self):
        signature = self._horizontal_signature(1, 22)
        frame = render_frame(self.cfg, self.state, [signature], [], 10.0)
        shadowish = sum(
            1 for r, g, b in frame.getdata()
            if 70 <= r <= 180 and 65 <= g <= 165 and 55 <= b <= 150 and abs(r - g) < 40
        )
        self.assertGreater(shadowish, 80)

    def test_flat_routes_do_not_invent_lift_shadow(self):
        flat = Route(3, tuple(RouteSegment(x, 5, "W", "N") for x in range(4, 12)), False, "resident", 800)
        frame = render_frame(self.cfg, self.state, [flat], [], 10.0)
        dark_warm = sum(
            1 for r, g, b in frame.getdata()
            if 85 <= r <= 130 and 75 <= g <= 120 and 65 <= b <= 105 and (r - b) >= 12 and (r - g) >= 5
        )
        self.assertLess(dark_warm, 20)

    def test_composition_has_a_real_quiet_pocket(self):
        signature = self._horizontal_signature(2, 28)
        residents = [
            Route(20 + y, tuple(RouteSegment(x, y, "W", "N") for x in range(2, 28)), False, "resident", 2600)
            for y in range(2, 9)
        ]
        frame = render_frame(self.cfg, self.state, [signature, *residents], [], 10.0)

        def luminance(box):
            x0, y0, x1, y1 = box
            vals = []
            for yy in range(y0, y1):
                for xx in range(x0, x1):
                    r, g, b = frame.getpixel((xx, yy))[:3]
                    vals.append((r + g + b) / 3)
            return sum(vals) / len(vals)

        pocket = luminance((285, 80, 500, 205))
        focus = luminance((570, 150, 820, 310))
        self.assertGreater(pocket, focus + 22)

    def test_weave_visually_builds_from_quiet_start_to_dense_climax(self):
        initial = build_initial_grid(self.cfg)
        events = build_cycle(self.cfg, initial)

        def frame_at(t):
            state = state_at(self.cfg, initial, events, t)
            routes = classify_routes(trace_routes(state), self.cfg)
            return render_frame(self.cfg, state, routes, assign_crossings(routes), t)

        def dark_count(frame):
            return sum(1 for r, g, b in frame.getdata() if (r + g + b) / 3 < 150)

        quiet = dark_count(frame_at(0.0))
        climax = dark_count(frame_at(9.5))
        self.assertGreater(climax, quiet * 1.35)

    def test_generated_composition_preserves_negative_space(self):
        initial = build_initial_grid(self.cfg)
        events = build_cycle(self.cfg, initial)
        state = state_at(self.cfg, initial, events, 10.0)
        routes = classify_routes(trace_routes(state), self.cfg)
        frame = render_frame(self.cfg, state, routes, assign_crossings(routes), 10.0)

        def luminance(box):
            x0, y0, x1, y1 = box
            vals = []
            for yy in range(y0, y1):
                for xx in range(x0, x1):
                    r, g, b = frame.getpixel((xx, yy))[:3]
                    vals.append((r + g + b) / 3)
            return sum(vals) / len(vals)

        quiet = luminance((300, 78, 500, 198))
        focus = luminance((560, 145, 835, 315))
        self.assertGreater(quiet, focus + 20)

    def test_lifted_span_visibly_leaves_its_flat_base_path(self):
        signature = self._horizontal_signature(9, 24)
        frame = render_frame(self.cfg, self.state, [signature], [], 10.0)
        points = _route_points(self.cfg, signature)
        top = _lifted_points(points, 6.2)
        start = int(len(points) * 0.24)
        mid = len(top) // 2
        bx, by = points[start + mid]
        tx, ty = top[mid]

        def near_graphite(cx, cy):
            count = 0
            for yy in range(round(cy) - 2, round(cy) + 3):
                for xx in range(round(cx) - 2, round(cx) + 3):
                    r, g, b = frame.getpixel((xx, yy))[:3]
                    if abs(r - self.cfg.graphite[0]) + abs(g - self.cfg.graphite[1]) + abs(b - self.cfg.graphite[2]) < 45:
                        count += 1
            return count

        self.assertLessEqual(near_graphite(bx, by), 3)
        self.assertGreaterEqual(near_graphite(tx, ty), 10)

    def test_lifted_ribbon_side_face_stays_subordinate_to_top_surface(self):
        signature = self._horizontal_signature(8, 24)
        frame = render_frame(self.cfg, self.state, [signature], [], 10.0)
        side = (63, 59, 53)
        graphite = self.cfg.graphite
        sideish = graphiteish = 0
        for r, g, b in frame.getdata():
            if abs(r - side[0]) + abs(g - side[1]) + abs(b - side[2]) < 30:
                sideish += 1
            if abs(r - graphite[0]) + abs(g - graphite[1]) + abs(b - graphite[2]) < 30:
                graphiteish += 1
        self.assertGreater(graphiteish, 0)
        self.assertLess(sideish / graphiteish, 0.20)

    @staticmethod
    def _horizontal_signature(route_id, length):
        segs = []
        x, y = 3, 5
        for i in range(length):
            entry, exit = (("W", "N") if i % 2 == 0 else ("S", "E"))
            segs.append(RouteSegment((x + i) % 29, y + (i % 2), entry, exit))
        return Route(route_id, tuple(segs), False, "signature", length * 100)


if __name__ == "__main__":
    unittest.main()
