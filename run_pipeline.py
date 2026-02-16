#!/usr/bin/env python3
"""Teams Call Summary Agent - Orchestrator pipeline."""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from ingest import validate_recording
from transcribe import transcribe as transcribe_audio
from agents import summarize, extract_deal, draft_email
from output import write_outputs

OLLAMA_BASE_URL = "http://localhost:11434/v1"
OLLAMA_DEFAULT_MODEL = "llama3:8b"


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Transcribe a Teams call, summarize it, extract deal insights, and draft an email to your manager."
    )
    parser.add_argument(
        "--recording",
        "-r",
        required=True,
        help="Path to the Teams recording file (.mp4, .webm, .mp3, etc.)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default="output",
        help="Directory for output files (default: output)",
    )
    parser.add_argument(
        "--model",
        "-m",
        default=None,
        help="Chat model for agents (default: gpt-4o-mini for cloud, llama3:8b for --local)",
    )
    parser.add_argument(
        "--local",
        "-l",
        action="store_true",
        help="Use local stack: faster-whisper for transcription, Ollama for summarize/extract/draft",
    )
    parser.add_argument(
        "--whisper-model",
        default="base",
        help="faster-whisper model size when using --local (default: base). Options: tiny, base, small, medium, large-v2, large-v3",
    )
    args = parser.parse_args()

    try:
        recording_path = validate_recording(args.recording)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    use_local = args.local
    if use_local:
        chat_model = args.model or os.getenv("OLLAMA_CHAT_MODEL", OLLAMA_DEFAULT_MODEL)
        llm_client = OpenAI(
            base_url=os.getenv("OLLAMA_BASE_URL", OLLAMA_BASE_URL),
            api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
        )
        print("Using local stack: faster-whisper + Ollama")
    else:
        chat_model = args.model or os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
        llm_client = OpenAI()
        print("Using cloud stack: OpenAI Whisper + OpenAI Chat")

    output_dir = Path(args.output_dir)

    print("Transcribing recording...")
    if use_local:
        transcript = transcribe_audio(
            recording_path,
            use_local=True,
            local_whisper_model=args.whisper_model,
        )
    else:
        transcript = transcribe_audio(recording_path, client=llm_client)
    if not transcript.strip():
        print("Error: Transcription produced no text.", file=sys.stderr)
        return 1
    print(f"Transcript length: {len(transcript)} chars")

    print("Summarizing call...")
    summary = summarize(transcript, client=llm_client, model=chat_model)

    print("Extracting deal insights...")
    deal_insights = extract_deal(
        transcript, summary=summary, client=llm_client, model=chat_model
    )

    print("Drafting email to manager...")
    email_draft = draft_email(
        summary, deal_insights, client=llm_client, model=chat_model
    )

    summary_path, deal_insights_path, email_path = write_outputs(
        summary, deal_insights, email_draft, output_dir
    )

    print(f"\nDone. Output files:")
    print(f"  Call summary: {summary_path}")
    print(f"  Deal insights: {deal_insights_path}")
    print(f"  Draft email: {email_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
