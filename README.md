# Teams Call Summary Agent

Automate **Teams recording → transcription → summary + deal/discount extraction → draft email to manager** with a single command.

## Features

- **Content-agnostic**: Analyzes whatever is discussed in the call—no hard-coded products or customers
- **Manual trigger**: Run when you're ready
- **Draft only**: Generates email for you to review and send (no auto-send)
- **Local + cloud**: Runs locally; uses OpenAI for transcription and LLM

## Setup

1. **Python 3.10+** required.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**: Copy `config.example.env` to `.env` and add your OpenAI API key:
   ```bash
   copy config.example.env .env
   ```
   Edit `.env` and set `OPENAI_API_KEY=sk-your-key`.

## Usage

```bash
python run_pipeline.py --recording path/to/recording.mp4
```

Options:

- `--recording` / `-r` – Path to the Teams recording (required)
- `--output-dir` / `-o` – Output directory (default: `output`)
- `--model` / `-m` – Chat model for agents (default: `gpt-4o-mini`)

### Supported formats

`.mp4`, `.webm`, `.mp3`, `.m4a`, `.wav`, `.ogg`

## Output

Creates three timestamped files in the output directory:

- `call_summary_YYYYMMDD_HHMM.txt` – The actual call summary (participants, topics, next steps)
- `deal_insights_YYYYMMDD_HHMM.txt` – Deal stage, discount requests, fit reasons
- `draft_email_to_manager_YYYYMMDD_HHMM.txt` – Ready to paste into Outlook

## Privacy

- API keys and output files stay local
- No email is sent automatically
- For internal use; you control what is shared
