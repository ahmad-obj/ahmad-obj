from __future__ import annotations

import argparse
from pathlib import Path

from .config import LoomConfig
from .export import _fixed_palette, _quantize, render_at


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--fps", type=int, required=True)
    parser.add_argument("--duration", type=float, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()

    config = LoomConfig(fps=args.fps, duration_s=args.duration, seed=args.seed)
    palette = _fixed_palette(config)
    args.directory.mkdir(parents=True, exist_ok=True)
    for index in range(args.start, args.end):
        frame = _quantize(render_at(config, index / config.fps), palette)
        frame.save(args.directory / f"frame_{index:04d}.png", compress_level=1)
        frame.close()


if __name__ == "__main__":
    main()
