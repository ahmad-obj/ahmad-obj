from __future__ import annotations

import math
import random
from typing import Iterable

from PIL import Image, ImageDraw, ImageFilter

from .config import LoomConfig
from .model import GridState
from .paths import Crossing, Route, RouteSegment, select_signature_routes


SCALE = 2


def _mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def _smoothstep(a: float, b: float, x: float) -> float:
    if a == b:
        return float(x >= b)
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3.0 - 2.0 * t)


def _layout(config: LoomConfig) -> tuple[float, float, float]:
    cell = 28.0
    field_w = config.cols * cell
    field_h = config.rows * cell
    x0 = (config.width - field_w) / 2.0
    y0 = (config.height - field_h) / 2.0 - 3.0
    return x0, y0, cell


def _point_for_side(x0: float, y0: float, cell: float, x: int, y: int, side: str) -> tuple[float, float]:
    cx = x0 + (x + 0.5) * cell
    cy = y0 + (y + 0.5) * cell
    r = cell / 2.0
    return {
        "N": (cx, cy - r),
        "E": (cx + r, cy),
        "S": (cx, cy + r),
        "W": (cx - r, cy),
    }[side]


def _corner_center(x0: float, y0: float, cell: float, seg: RouteSegment) -> tuple[float, float]:
    cx = x0 + (seg.x + 0.5) * cell
    cy = y0 + (seg.y + 0.5) * cell
    r = cell / 2.0
    pair = frozenset((seg.entry, seg.exit))
    if pair == frozenset(("N", "E")):
        return cx + r, cy - r
    if pair == frozenset(("N", "W")):
        return cx - r, cy - r
    if pair == frozenset(("S", "E")):
        return cx + r, cy + r
    if pair == frozenset(("S", "W")):
        return cx - r, cy + r
    raise ValueError(f"invalid quarter-turn segment: {seg}")


def _arc_points(config: LoomConfig, seg: RouteSegment, samples: int = 10) -> list[tuple[float, float]]:
    x0, y0, cell = _layout(config)
    start = _point_for_side(x0, y0, cell, seg.x, seg.y, seg.entry)
    end = _point_for_side(x0, y0, cell, seg.x, seg.y, seg.exit)
    ox, oy = _corner_center(x0, y0, cell, seg)
    radius = cell / 2.0
    a0 = math.atan2(start[1] - oy, start[0] - ox)
    a1 = math.atan2(end[1] - oy, end[0] - ox)
    delta = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    if abs(delta) > math.pi / 2 + 0.01:
        delta = -math.copysign(2 * math.pi - abs(delta), delta)
    return [
        (ox + radius * math.cos(a0 + delta * i / samples), oy + radius * math.sin(a0 + delta * i / samples))
        for i in range(samples + 1)
    ]


def _route_points(config: LoomConfig, route: Route) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for idx, seg in enumerate(route.segments):
        arc = _arc_points(config, seg)
        if idx and points and arc:
            if math.dist(points[-1], arc[-1]) < math.dist(points[-1], arc[0]):
                arc.reverse()
            if math.dist(points[-1], arc[0]) < 0.5:
                arc = arc[1:]
        points.extend(arc)
    return points


def _scaled(points: Iterable[tuple[float, float]], dx: float = 0.0, dy: float = 0.0) -> list[tuple[int, int]]:
    return [(round((x + dx) * SCALE), round((y + dy) * SCALE)) for x, y in points]


def _tier(route: Route, config: LoomConfig) -> str:
    if route.tier:
        return route.tier
    if route.length <= config.whisper_max:
        return "whisper"
    if route.length <= config.resident_max:
        return "resident"
    if route.length <= config.major_max:
        return "major"
    return "signature"


def _weave_strength(t: float, duration: float) -> float:
    phase = (t % duration) / duration
    return math.sin(math.pi * phase) ** 2


def _route_style(config: LoomConfig, route: Route, t: float) -> tuple[tuple[int, int, int], float]:
    tier = _tier(route, config)
    if tier == "whisper":
        color, width = _mix(config.vellum, config.graphite, 0.26), 2.4
    elif tier == "resident":
        color, width = _mix(config.vellum, config.graphite, 0.62), 3.2
    elif tier == "major":
        color, width = _mix(config.graphite, config.charcoal, 0.12), 4.7
    else:
        color, width = config.graphite, 7.0

    weave = _weave_strength(t, config.duration_s)
    base_visibility = {"whisper": 0.08, "resident": 0.16, "major": 0.26, "signature": 0.34}[tier]
    visibility = base_visibility + (1.0 - base_visibility) * weave
    color = _mix(config.vellum, color, visibility)

    if route.segments and tier in {"whisper", "resident"}:
        mx = sum(s.x for s in route.segments) / len(route.segments)
        my = sum(s.y for s in route.segments) / len(route.segments)
        if mx < config.cols * 0.34 and my < config.rows * 0.38:
            color = _mix(config.vellum, color, 0.45)
    return color, width


def _lift_strength(t: float, duration: float) -> float:
    t = t % duration
    if t < 5.5:
        return 0.0
    if t < 9.5:
        return _smoothstep(5.5, 9.5, t)
    if t < 12.0:
        return 1.0
    if t < 16.3:
        return 1.0 - 0.72 * _smoothstep(12.0, 16.3, t)
    return 0.28 * (1.0 - _smoothstep(16.3, duration, t))


def _draw_line(draw: ImageDraw.ImageDraw, points, fill, width: float) -> None:
    if len(points) >= 2:
        draw.line(points, fill=fill, width=max(1, round(width * SCALE)), joint="curve")


def _lifted_points(points: list[tuple[float, float]], elevation: float) -> list[tuple[float, float]]:
    if len(points) < 4:
        return points
    start = int(len(points) * 0.24)
    end = max(start + 2, int(len(points) * 0.78))
    lifted = []
    for i in range(start, end):
        u = (i - start) / max(1, end - start - 1)
        rise = elevation * math.sin(math.pi * u) ** 1.3
        x, y = points[i]
        lifted.append((x, y - rise))
    return lifted


def _draw_lifted(base: Image.Image, config: LoomConfig, route: Route, t: float, strength: float) -> list[tuple[float, float]]:
    points = _route_points(config, route)
    if not points or strength <= 0.03:
        return []
    tier = _tier(route, config)
    elevation = (6.2 if tier == "signature" else 2.6) * strength
    top = _lifted_points(points, elevation)
    if len(top) < 2:
        return []

    width = 7.0 if tier == "signature" else 4.7
    start = int(len(points) * 0.24)
    end = min(len(points), start + len(top))
    base_span = points[start:end]

    draw = ImageDraw.Draw(base)
    _draw_line(draw, _scaled(base_span), (*config.vellum, 255), width + 1.2)

    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    shadow_color = (*config.shadow, round(72 * strength))
    _draw_line(sd, _scaled(base_span, 2.5 * strength, 4.0 * strength), shadow_color, width + 2.4)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=3.0 * SCALE))
    base.alpha_composite(shadow)

    side = _mix(config.graphite, config.shadow, 0.52)
    _draw_line(draw, _scaled(base_span), (*side, round(108 * strength)), 1.8)
    _draw_line(draw, _scaled(top), (*config.graphite, 255), width)
    highlight = [(x, y - 0.7) for x, y in top]
    _draw_line(draw, _scaled(highlight), (*config.highlight, 120), 0.9)
    return top


def _apply_quiet_pocket(base: Image.Image, config: LoomConfig) -> None:
    veil = Image.new("RGBA", base.size, (*config.vellum, 0))
    mask = Image.new("L", base.size, 0)
    md = ImageDraw.Draw(mask)
    box = tuple(v * SCALE for v in (286, 66, 516, 214))
    md.ellipse(box, fill=218)
    mask = mask.filter(ImageFilter.GaussianBlur(18 * SCALE))
    veil.putalpha(mask)
    base.alpha_composite(veil)


def _draw_transition_tiles(base: Image.Image, config: LoomConfig, state: GridState) -> None:
    if not state.transitions:
        return
    draw = ImageDraw.Draw(base)
    for (x, y), progress in state.transitions.items():
        target = 1 - state.cells[y][x]
        alpha = max(0.0, min(1.0, progress))
        pairs = (("N", "W"), ("S", "E")) if target else (("N", "E"), ("S", "W"))
        color = _mix(config.vellum, config.charcoal, 0.18 + 0.42 * alpha)
        for entry, exit in pairs:
            pts = _arc_points(config, RouteSegment(x, y, entry, exit), samples=12)
            _draw_line(draw, _scaled(pts), (*color, round(150 * alpha)), 2.4)


def _apply_static_grain(image: Image.Image, config: LoomConfig) -> Image.Image:
    rgb = image.convert("RGB")
    pixels = rgb.load()
    rng = random.Random(config.seed ^ 0xA11CE)
    for y in range(0, config.height, 2):
        for x in range(0, config.width, 2):
            if rng.random() < 0.23:
                d = rng.choice((-1, 1))
                for yy in range(y, min(config.height, y + 2)):
                    for xx in range(x, min(config.width, x + 2)):
                        r, g, b = pixels[xx, yy]
                        pixels[xx, yy] = (
                            max(0, min(255, r + d)),
                            max(0, min(255, g + d)),
                            max(0, min(255, b + d)),
                        )
    return rgb


def render_frame(
    config: LoomConfig,
    state: GridState,
    routes: list[Route],
    crossings: list[Crossing],
    t: float,
) -> Image.Image:
    canvas = Image.new("RGBA", (config.width * SCALE, config.height * SCALE), (*config.vellum, 255))
    draw = ImageDraw.Draw(canvas)

    ordered = sorted(routes, key=lambda r: ({"whisper": 0, "resident": 1, "major": 2, "signature": 3}.get(_tier(r, config), 0), r.score, r.route_id))
    for route in ordered:
        points = _route_points(config, route)
        color, width = _route_style(config, route, t)
        _draw_line(draw, _scaled(points), (*color, 255), width)

    _apply_quiet_pocket(canvas, config)
    _draw_transition_tiles(canvas, config, state)

    lift = _lift_strength(t, config.duration_s)
    signatures = select_signature_routes(ordered, min(config.signature_limit, 2))
    if not signatures:
        signatures = sorted([r for r in ordered if _tier(r, config) == "signature"], key=lambda r: (-r.length, r.route_id))[:2]
    major = sorted([r for r in ordered if _tier(r, config) == "major"], key=lambda r: (-r.score, r.route_id))[:1]

    lifted_ids: set[int] = set()
    lifted_paths: dict[int, list[tuple[float, float]]] = {}
    for route in major:
        top = _draw_lifted(canvas, config, route, t, lift * 0.54)
        if top:
            lifted_ids.add(route.route_id)
            lifted_paths[route.route_id] = top
    for route in signatures:
        top = _draw_lifted(canvas, config, route, t, lift)
        if top:
            lifted_ids.add(route.route_id)
            lifted_paths[route.route_id] = top

    if lift > 0.15 and crossings:
        cross_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        cd = ImageDraw.Draw(cross_layer)
        x0, y0, cell = _layout(config)
        count = 0
        for crossing in crossings:
            if crossing.upper_route_id not in lifted_ids:
                continue
            cx = (x0 + (crossing.x + 0.5) * cell) * SCALE
            cy = (y0 + (crossing.y + 0.5) * cell + 3.0 * lift) * SCALE
            rr = 6.0 * SCALE
            cd.ellipse((cx - rr, cy - rr * 0.45, cx + rr, cy + rr * 0.45), fill=(*config.shadow, round(32 * lift)))
            count += 1
            if count >= 6:
                break
        if count:
            cross_layer = cross_layer.filter(ImageFilter.GaussianBlur(2.2 * SCALE))
            canvas.alpha_composite(cross_layer)

    if lifted_paths and 2.5 <= (t % config.duration_s) <= 15.2:
        route_id = sorted(lifted_paths)[0]
        top = lifted_paths[route_id]
        if len(top) > 6:
            phase = ((t - 2.5) / 12.7) % 1.0
            span = max(3, int(len(top) * 0.035))
            start = min(len(top) - span - 1, max(0, int(phase * (len(top) - span - 1))))
            accent = top[start : start + span]
            ad = ImageDraw.Draw(canvas)
            _draw_line(ad, _scaled(accent), (*config.ultramarine, 240), 1.9)

    canvas = canvas.resize((config.width, config.height), Image.Resampling.LANCZOS)
    return _apply_static_grain(canvas, config)
