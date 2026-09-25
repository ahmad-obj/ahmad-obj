from __future__ import annotations

import argparse
from pathlib import Path

from .config import LoomConfig
from .export import _save_poster, export_animation


def main() -> None:
    parser = argparse.ArgumentParser(description="Render The Loom GitHub profile artwork")
    parser.add_argument("--output", type=Path, help="Animated GIF destination")
    parser.add_argument("--poster", type=Path, help="Poster PNG destination")
    parser.add_argument("--seed", type=int, default=20260925)
    args = parser.parse_args()

    if not args.output and not args.poster:
        parser.error("provide --output and/or --poster")

    config = LoomConfig(seed=args.seed)
    if args.output:
        result = export_animation(config, args.output, args.poster)
        print(f"{result.frame_count} frames | {result.size_bytes / 1024 / 1024:.2f} MB | {result.sha256}")
    elif args.poster:
        _save_poster(config, args.poster)
        print(f"poster: {args.poster}")


if __name__ == "__main__":
    main()
