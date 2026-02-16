"""Extract deal and discount insights from transcript/summary."""

from openai import OpenAI

SYSTEM_PROMPT = """You are an assistant that extracts deal and sales insights from call transcripts.
From the provided summary/transcript, list:
1. Deal stage or interest level
2. Any discount or pricing requests
3. Reasons the customer is a good fit (e.g. existing relationship, current stack)
Base everything on what was actually said—do not assume a specific product or invent context."""


def extract_deal(
    transcript: str,
    summary: str | None = None,
    client: OpenAI | None = None,
    model: str = "gpt-4o-mini",
) -> str:
    """Extract deal stage, discount needs, and fit reasons."""
    client = client or OpenAI()
    content = summary if summary else transcript
    if summary and transcript:
        content = f"Summary:\n{summary}\n\nFull transcript (for reference):\n{transcript}"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
