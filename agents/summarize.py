"""Summarize call transcript."""

from openai import OpenAI

SYSTEM_PROMPT = """You are an assistant that summarizes sales/customer calls. 
Summarize the transcript concisely. Include:
- Who was on the call (if identifiable)
- Main topics and products/solutions discussed
- The customer's current situation or existing tools (if mentioned)
- Any objections, questions, or next steps
Base everything on what was actually said—do not assume or invent content."""


def summarize(
    transcript: str,
    client: OpenAI | None = None,
    model: str = "gpt-4o-mini",
) -> str:
    """Generate a structured summary of the call."""
    client = client or OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
