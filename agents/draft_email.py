"""Draft email to manager based on call summary and deal insights."""

from openai import OpenAI

SYSTEM_PROMPT = """You are an assistant that drafts professional emails to managers about sales calls.
Write a short email to my manager with:
- A brief call summary
- Deal potential
- Suggested discount/offerings based on what was discussed
Keep tone professional and concise. Do not invent products or context not present in the call."""


def draft_email(
    summary: str,
    deal_insights: str,
    client: OpenAI | None = None,
    model: str = "gpt-4o-mini",
) -> str:
    """Generate a draft email for the manager."""
    client = client or OpenAI()
    content = f"""Call summary:
{summary}

Deal insights:
{deal_insights}

Draft a professional email to my manager covering the above."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()
