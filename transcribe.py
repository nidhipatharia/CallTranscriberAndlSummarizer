"""Transcribe audio/video using OpenAI Whisper API or local faster-whisper."""

from pathlib import Path

from openai import OpenAI


def transcribe(
    file_path: Path,
    client: OpenAI | None = None,
    model: str = "whisper-1",
    use_local: bool = False,
    local_whisper_model: str = "base",
) -> str:
    """Transcribe the audio/video file and return the full transcript text."""
    if use_local:
        return _transcribe_local(file_path, model_size=local_whisper_model)
    client = client or OpenAI()
    with open(file_path, "rb") as f:
        response = client.audio.transcriptions.create(
            model=model,
            file=f,
            response_format="text",
        )
    return response if isinstance(response, str) else response.text


def _transcribe_local(file_path: Path, model_size: str = "base") -> str:
    """Transcribe using local faster-whisper (no API key required)."""
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(str(file_path), beam_size=5)
    return " ".join(seg.text for seg in segments).strip()
