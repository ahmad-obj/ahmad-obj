from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile
import sys

from PIL import Image

from .config import LoomConfig
from .model import build_cycle, build_initial_grid, state_at
from .paths import assign_crossings, classify_routes, trace_routes
from .render import _mix, render_frame


@dataclass(frozen=True)
class ExportResult:
    path: Path
    frame_count: int
    size_bytes: int
    sha256: str


def render_at(config: LoomConfig, t: float) -> Image.Image:
    initial = build_initial_grid(config)
    events = build_cycle(config, initial)
    state = state_at(config, initial, events, t)
    routes = classify_routes(trace_routes(state), config)
    crossings = assign_crossings(routes)
    return render_frame(config, state, routes, crossings, t)


def _fixed_palette(config: LoomConfig) -> Image.Image:
    colors: list[tuple[int, int, int]] = []
    for i in range(32):
        colors.append(_mix(config.vellum, config.graphite, i / 31))
    for i in range(12):
        colors.append(_mix(config.vellum, config.shadow, i / 11))
    for i in range(10):
        colors.append(_mix(config.vellum, config.ultramarine, i / 9))
    colors.extend([
        config.highlight,
        config.vellum_alt,
        tuple(max(0, c - 1) for c in config.vellum),
        tuple(min(255, c + 1) for c in config.vellum),
    ])
    colors = colors[:64]
    colors.extend([config.vellum] * (256 - len(colors)))
    palette = Image.new("P", (1, 1))
    palette.putpalette([channel for color in colors for channel in color])
    return palette


def _quantize(frame: Image.Image, palette: Image.Image) -> Image.Image:
    return frame.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE)


def _save_poster(config: LoomConfig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    poster = render_at(config, 10.0)
    poster_q = poster.quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    poster_q.save(path, optimize=True)


def _encode_gif(config: LoomConfig, frame_pattern: str, output: Path) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg is required to encode The Loom GIF")
    command = [
        ffmpeg,
        "-v", "error",
        "-y",
        "-framerate", str(config.fps),
        "-i", frame_pattern,
        "-loop", "0",
        "-map_metadata", "-1",
        str(output),
    ]
    subprocess.run(command, check=True)


def export_animation(config: LoomConfig, output_path: str | Path, poster_path: str | Path | None = None) -> ExportResult:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame_count = round(config.duration_s * config.fps)

    with tempfile.TemporaryDirectory(prefix="loom-frames-") as tmp:
        tmp_path = Path(tmp)
        batch_size = 18
        repo_root = Path(__file__).resolve().parents[2]
        for start in range(0, frame_count, batch_size):
            end = min(frame_count, start + batch_size)
            command = [
                sys.executable, "-m", "tools.loom.worker",
                "--start", str(start),
                "--end", str(end),
                "--directory", str(tmp_path),
                "--fps", str(config.fps),
                "--duration", str(config.duration_s),
                "--seed", str(config.seed),
            ]
            subprocess.run(command, check=True, cwd=repo_root)
        _encode_gif(config, str(tmp_path / "frame_%04d.png"), output)

    if poster_path is not None:
        _save_poster(config, Path(poster_path))

    size = output.stat().st_size
    if size > 10 * 1024 * 1024:
        output.unlink(missing_ok=True)
        raise ValueError(f"The Loom export exceeds 10 MB hard cap: {size / 1024 / 1024:.2f} MB")

    sha = hashlib.sha256(output.read_bytes()).hexdigest()
    return ExportResult(output, frame_count, size, sha)
