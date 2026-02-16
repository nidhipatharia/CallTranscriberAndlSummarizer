"""Write summary, deal insights, and draft email to separate files."""

from pathlib import Path
from datetime import datetime


def write_outputs(
    summary: str,
    deal_insights: str,
    draft_email: str,
    output_dir: Path,
) -> tuple[Path, Path, Path]:
    """Write call summary, deal insights, and draft email to separate timestamped files.
    Returns paths to created files: (summary_path, deal_insights_path, email_path).
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")

    # Call summary only - the actual LLM-generated summary of the call
    summary_path = output_dir / f"call_summary_{ts}.txt"
    summary_path.write_text(summary, encoding="utf-8")

    # Deal insights only
    deal_insights_path = output_dir / f"deal_insights_{ts}.txt"
    deal_insights_path.write_text(deal_insights, encoding="utf-8")

    # Draft email to manager
    email_path = output_dir / f"draft_email_to_manager_{ts}.txt"
    email_path.write_text(draft_email, encoding="utf-8")

    return summary_path, deal_insights_path, email_path
