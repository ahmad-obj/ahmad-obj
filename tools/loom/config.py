from dataclasses import dataclass


@dataclass(frozen=True)
class LoomConfig:
    width: int = 1200
    height: int = 430
    cols: int = 30
    rows: int = 11
    duration_s: float = 18.0
    fps: int = 12
    seed: int = 20260925
    transition_s: float = 0.55
    vellum: tuple[int, int, int] = (243, 239, 230)
    vellum_alt: tuple[int, int, int] = (239, 234, 223)
    graphite: tuple[int, int, int] = (25, 26, 28)
    charcoal: tuple[int, int, int] = (79, 74, 68)
    ultramarine: tuple[int, int, int] = (45, 79, 184)
    shadow: tuple[int, int, int] = (99, 89, 77)
    highlight: tuple[int, int, int] = (248, 244, 236)
    whisper_max: int = 4
    resident_max: int = 10
    major_max: int = 18
    signature_limit: int = 3
