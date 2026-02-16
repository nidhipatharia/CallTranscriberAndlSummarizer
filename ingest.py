"""Validate and prepare recording file for transcription."""

import os
from pathlib import Path

SUPPORTED_EXTENSIONS = {".mp4", ".webm", ".mp3", ".m4a", ".wav", ".ogg"}
MAX_SIZE_MB = 500


def validate_recording(path: str | Path) -> Path:
    """Validate the recording file exists, has a supported format, and reasonable size."""
    p = Path(path).resolve()
    if not p.exists():
        raise FileNotFoundError(f"Recording file not found: {p}")
    if not p.is_file():
        raise ValueError(f"Path is not a file: {p}")
    if p.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported format: {p.suffix}. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    size_mb = p.stat().st_size / (1024 * 1024)
    if size_mb > MAX_SIZE_MB:
        raise ValueError(f"File too large: {size_mb:.1f} MB (max {MAX_SIZE_MB} MB)")
    return p
