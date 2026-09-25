from __future__ import annotations

from dataclasses import dataclass, replace
from collections import defaultdict

from .config import LoomConfig
from .model import GridState


SIDES = ("N", "E", "S", "W")
OPPOSITE = {"N": "S", "E": "W", "S": "N", "W": "E"}
DELTA = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
TILE_PAIRS = {
    0: (("N", "E"), ("S", "W")),
    1: (("N", "W"), ("S", "E")),
}
TIER_RANK = {None: 0, "whisper": 1, "resident": 2, "major": 3, "signature": 4}


@dataclass(frozen=True)
class RouteSegment:
    x: int
    y: int
    entry: str
    exit: str


@dataclass(frozen=True)
class Route:
    route_id: int
    segments: tuple[RouteSegment, ...]
    closed: bool
    tier: str | None = None
    score: float = 0.0

    @property
    def length(self) -> int:
        return len(self.segments)


@dataclass(frozen=True)
class Crossing:
    x: int
    y: int
    upper_route_id: int
    lower_route_id: int


def _is_boundary_half_edge(x: int, y: int, side: str, grid: GridState) -> bool:
    return (
        (side == "N" and y == 0)
        or (side == "S" and y == grid.rows - 1)
        or (side == "W" and x == 0)
        or (side == "E" and x == grid.cols - 1)
    )


def trace_routes(grid: GridState) -> list[Route]:
    if grid.cols <= 0 or grid.rows <= 0:
        return []

    arc_data: dict[tuple[int, int, int], tuple[int, int, str, str]] = {}
    half_to_arc: dict[tuple[int, int, str], tuple[int, int, int]] = {}
    for y, row in enumerate(grid.cells):
        for x, state in enumerate(row):
            for pair_idx, (a, b) in enumerate(TILE_PAIRS[int(state)]):
                arc_id = (y, x, pair_idx)
                arc_data[arc_id] = (x, y, a, b)
                half_to_arc[(x, y, a)] = arc_id
                half_to_arc[(x, y, b)] = arc_id

    unvisited = set(arc_data)
    routes: list[Route] = []

    def choose_start() -> tuple[tuple[int, int, int], str]:
        boundary_options: list[tuple[tuple[int, int, int], str]] = []
        for arc_id in sorted(unvisited):
            x, y, a, b = arc_data[arc_id]
            if _is_boundary_half_edge(x, y, a, grid):
                boundary_options.append((arc_id, a))
            if _is_boundary_half_edge(x, y, b, grid):
                boundary_options.append((arc_id, b))
        if boundary_options:
            return min(boundary_options, key=lambda item: (item[0], item[1]))
        arc_id = min(unvisited)
        return arc_id, arc_data[arc_id][2]

    while unvisited:
        first_arc, first_entry = choose_start()
        current_arc = first_arc
        entry = first_entry
        segments: list[RouteSegment] = []
        closed = False

        while True:
            x, y, a, b = arc_data[current_arc]
            exit_side = b if entry == a else a
            segments.append(RouteSegment(x, y, entry, exit_side))
            unvisited.discard(current_arc)

            if _is_boundary_half_edge(x, y, exit_side, grid):
                break

            dx, dy = DELTA[exit_side]
            nx, ny = x + dx, y + dy
            next_entry = OPPOSITE[exit_side]
            next_arc = half_to_arc[(nx, ny, next_entry)]

            if next_arc == first_arc and next_entry == first_entry:
                closed = True
                break
            if next_arc not in unvisited:
                break

            current_arc = next_arc
            entry = next_entry

        routes.append(Route(len(routes), tuple(segments), closed))

    return routes


def classify_routes(routes: list[Route], config: LoomConfig) -> list[Route]:
    classified: list[Route] = []
    for route in routes:
        n = route.length
        if n <= config.whisper_max:
            tier = "whisper"
        elif n <= config.resident_max:
            tier = "resident"
        elif n <= config.major_max:
            tier = "major"
        else:
            tier = "signature"

        if route.segments:
            mean_x = sum(s.x for s in route.segments) / (len(route.segments) * max(1, config.cols - 1))
            mean_y = sum(s.y for s in route.segments) / (len(route.segments) * max(1, config.rows - 1))
        else:
            mean_x = mean_y = 0.5
        focus_bonus = 8.0 if 0.48 <= mean_x <= 0.84 and 0.22 <= mean_y <= 0.82 else 0.0
        quiet_penalty = 6.0 if mean_x < 0.33 and mean_y < 0.38 else 0.0
        score = n * 100.0 + focus_bonus - quiet_penalty
        classified.append(replace(route, tier=tier, score=score))
    return classified


def select_signature_routes(routes: list[Route], limit: int = 3) -> list[Route]:
    signatures = [route for route in routes if route.tier == "signature"]
    signatures.sort(key=lambda route: (-route.score, -route.length, route.route_id))
    return signatures[: max(0, min(limit, 3))]


def assign_crossings(routes: list[Route]) -> list[Crossing]:
    by_cell: dict[tuple[int, int], list[Route]] = defaultdict(list)
    for route in routes:
        seen = set()
        for segment in route.segments:
            cell = (segment.x, segment.y)
            if cell not in seen:
                by_cell[cell].append(route)
                seen.add(cell)

    crossings: list[Crossing] = []
    for (x, y), cell_routes in sorted(by_cell.items()):
        unique = {route.route_id: route for route in cell_routes}
        if len(unique) < 2:
            continue
        ranked = sorted(
            unique.values(),
            key=lambda route: (-TIER_RANK[route.tier], -route.score, route.route_id),
        )
        upper = ranked[0]
        for lower in ranked[1:2]:
            crossings.append(Crossing(x, y, upper.route_id, lower.route_id))
    return crossings
