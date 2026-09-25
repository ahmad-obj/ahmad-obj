from __future__ import annotations

from dataclasses import dataclass, field
import math
import random

from .config import LoomConfig


Cell = tuple[int, int]


@dataclass(frozen=True)
class MutationEvent:
    time: float
    zone: str
    cells: tuple[Cell, ...]


@dataclass(frozen=True)
class GridState:
    cols: int
    rows: int
    cells: tuple[tuple[int, ...], ...]
    transitions: dict[Cell, float] = field(default_factory=dict, compare=True)


def build_initial_grid(config: LoomConfig) -> GridState:
    rng = random.Random(config.seed)
    rows: list[tuple[int, ...]] = []
    for y in range(config.rows):
        row = []
        for x in range(config.cols):
            nx = x / max(1, config.cols - 1)
            ny = y / max(1, config.rows - 1)
            bias = (
                0.52 * math.sin(nx * math.tau * 1.35 + 0.35)
                + 0.31 * math.cos(ny * math.tau * 0.95 - 0.7)
                + 0.23 * math.sin((nx + ny) * math.tau * 0.72)
            )
            noise = rng.uniform(-0.64, 0.64)
            row.append(1 if bias + noise > 0 else 0)
        rows.append(tuple(row))
    return GridState(config.cols, config.rows, tuple(rows), {})


def _zone_cells(config: LoomConfig, rng: random.Random, center: tuple[float, float], count: int) -> tuple[Cell, ...]:
    cx, cy = center
    candidates: list[tuple[float, Cell]] = []
    for y in range(config.rows):
        for x in range(config.cols):
            d = ((x - cx) / 4.3) ** 2 + ((y - cy) / 2.2) ** 2
            jitter = rng.random() * 0.42
            candidates.append((d + jitter, (x, y)))
    candidates.sort(key=lambda item: item[0])
    chosen = [cell for _, cell in candidates[: max(count * 3, count)]]
    rng.shuffle(chosen)
    return tuple(sorted(chosen[:count]))


def build_cycle(config: LoomConfig, grid: GridState) -> list[MutationEvent]:
    rng = random.Random(config.seed ^ 0x5EEDBEEF)
    specs = [
        ("primary", 1.20, 10.10, (8.0, 6.7), (19.0, 4.7), 6),
        ("secondary", 3.35, 13.30, (21.5, 3.2), (10.8, 7.2), 5),
        ("repair", 6.20, 15.55, (14.2, 7.4), (23.8, 7.6), 4),
        ("primary", 5.10, 12.25, (12.0, 4.0), (18.0, 7.0), 3),
        ("secondary", 7.40, 14.60, (24.0, 5.8), (6.0, 4.8), 4),
        ("repair", 9.10, 16.30, (17.5, 3.5), (14.0, 6.4), 3),
    ]
    events: list[MutationEvent] = []
    for zone, start, end, c0, c1, count in specs:
        center = c0 if rng.random() < 0.5 else c1
        cells = _zone_cells(config, rng, center, count)
        events.append(MutationEvent(start, zone, cells))
        events.append(MutationEvent(end, zone, cells))
    events.sort(key=lambda e: (e.time, e.zone, e.cells))
    return events


def state_at(config: LoomConfig, initial: GridState, events: list[MutationEvent], t: float) -> GridState:
    if math.isclose(t, config.duration_s, abs_tol=1e-9):
        return initial
    t = t % config.duration_s
    cells = [list(row) for row in initial.cells]
    transitions: dict[Cell, float] = {}
    for event in events:
        dt = t - event.time
        if dt >= config.transition_s:
            for x, y in event.cells:
                cells[y][x] ^= 1
        elif 0.0 < dt < config.transition_s:
            progress = dt / config.transition_s
            for cell in event.cells:
                transitions[cell] = progress
    return GridState(initial.cols, initial.rows, tuple(tuple(row) for row in cells), transitions)
