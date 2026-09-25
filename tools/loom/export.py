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


def _delivery_height(config: LoomConfig, width: int) -> int:
    return round(width * config.height / config.width)


def _encode_webp(
    frame_pattern: str,
    output: Path,
    source_fps: int,
    width: int,
    height: int,
    quality: int,
) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg is required to encode The Loom WebP")
    command = [
        ffmpeg,
        "-v", "error",
        "-y",
        "-framerate", str(source_fps),
        "-i", frame_pattern,
        "-vf", f"scale={width}:{height}:flags=lanczos",
        "-c:v", "libwebp",
        "-lossless", "0",
        "-q:v", str(quality),
        "-compression_level", "6",
        "-preset", "picture",
        "-loop", "0",
        "-an",
        "-map_metadata", "-1",
        str(output),
    ]
    subprocess.run(command, check=True)


def _encode_delivery_gif(
    frame_pattern: str,
    output: Path,
    source_fps: int,
    gif_fps: int,
    width: int,
    height: int,
) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg is required to encode The Loom GIF")
    filters = (
        f"[0:v]fps={gif_fps},scale={width}:{height}:flags=lanczos,split[a][b];"
        "[a]palettegen=max_colors=96:stats_mode=diff[p];"
        "[b][p]paletteuse=dither=none:diff_mode=rectangle"
    )
    command = [
        ffmpeg,
        "-v", "error",
        "-y",
        "-framerate", str(source_fps),
        "-i", frame_pattern,
        "-filter_complex", filters,
        "-loop", "0",
        "-map_metadata", "-1",
        str(output),
    ]
    subprocess.run(command, check=True)


def export_delivery_assets(
    config: LoomConfig,
    webp_path: str | Path,
    gif_path: str | Path,
    *,
    duration_s: float | None = None,
    webp_fps: int | None = None,
    gif_fps: int | None = None,
    width: int | None = None,
    gif_width: int | None = None,
) -> dict[str, ExportResult]:
    duration = config.duration_s if duration_s is None else duration_s
    source_fps = config.webp_fps if webp_fps is None else webp_fps
    fallback_fps = config.gif_fps if gif_fps is None else gif_fps
    delivery_width = config.delivery_width if width is None else width
    delivery_height = _delivery_height(config, delivery_width)
    fallback_width = config.gif_width if gif_width is None else gif_width
    fallback_height = _delivery_height(config, fallback_width)
    webp = Path(webp_path)
    gif = Path(gif_path)
    webp.parent.mkdir(parents=True, exist_ok=True)
    gif.parent.mkdir(parents=True, exist_ok=True)
    frame_count = round(duration * source_fps)

    with tempfile.TemporaryDirectory(prefix="loom-delivery-") as tmp:
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
                "--fps", str(source_fps),
                "--duration", str(duration),
                "--seed", str(config.seed),
            ]
            subprocess.run(command, check=True, cwd=repo_root)

        pattern = str(tmp_path / "frame_%04d.png")
        _encode_webp(pattern, webp, source_fps, delivery_width, delivery_height, config.webp_quality)
        _encode_delivery_gif(pattern, gif, source_fps, fallback_fps, fallback_width, fallback_height)

    webp_size = webp.stat().st_size
    gif_size = gif.stat().st_size
    if webp_size > 5 * 1024 * 1024:
        raise ValueError(f"The Loom WebP exceeds 5 MB delivery cap: {webp_size / 1024 / 1024:.2f} MB")
    if gif_size > 5 * 1024 * 1024:
        raise ValueError(f"The Loom fallback GIF exceeds 5 MB delivery cap: {gif_size / 1024 / 1024:.2f} MB")

    return {
        "webp": ExportResult(webp, frame_count, webp_size, hashlib.sha256(webp.read_bytes()).hexdigest()),
        "gif": ExportResult(gif, round(duration * fallback_fps), gif_size, hashlib.sha256(gif.read_bytes()).hexdigest()),
    }
