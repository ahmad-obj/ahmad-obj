from __future__ import annotations

import argparse
from pathlib import Path

from .config import LoomConfig
from .export import _save_poster, export_animation, export_delivery_assets


def main() -> None:
    parser = argparse.ArgumentParser(description="Render The Loom GitHub profile artwork")
    parser.add_argument("--output", type=Path, help="Legacy full-size animated GIF destination")
    parser.add_argument("--webp", type=Path, help="Preferred optimized animated WebP destination")
    parser.add_argument("--gif", type=Path, help="Optimized GIF fallback destination")
    parser.add_argument("--poster", type=Path, help="Poster PNG destination")
    parser.add_argument("--seed", type=int, default=20260925)
    args = parser.parse_args()

    if not any((args.output, args.webp, args.gif, args.poster)):
        parser.error("provide --webp/--gif, --output, and/or --poster")
    if bool(args.webp) != bool(args.gif):
        parser.error("--webp and --gif must be provided together")

    config = LoomConfig(seed=args.seed)
    if args.webp and args.gif:
        results = export_delivery_assets(config, args.webp, args.gif)
        if args.poster:
            _save_poster(config, args.poster)
        webp = results["webp"]
        gif = results["gif"]
        print(
            f"webp: {webp.frame_count} frames | {webp.size_bytes / 1024 / 1024:.2f} MB | {webp.sha256}\n"
            f"gif: {gif.frame_count} frames | {gif.size_bytes / 1024 / 1024:.2f} MB | {gif.sha256}"
        )
    elif args.output:
        result = export_animation(config, args.output, args.poster)
        print(f"{result.frame_count} frames | {result.size_bytes / 1024 / 1024:.2f} MB | {result.sha256}")
    elif args.poster:
        _save_poster(config, args.poster)
        print(f"poster: {args.poster}")


if __name__ == "__main__":
    main()
