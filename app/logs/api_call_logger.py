"""Log OpenAI API calls: developer prompt, user prompt, and token usage."""

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

LOGS_DIR = Path(__file__).resolve().parent
IST = ZoneInfo("Asia/Kolkata")


def log_api_call(
    call_type: str,
    developer_prompt: str,
    user_prompt: str,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
) -> None:
    """Write one API call log to a timestamped file under app/logs."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(IST)
    filename = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}-{now.microsecond:06d}_ist.log"
    filepath = LOGS_DIR / filename

    lines = [
        "=" * 80,
        f"API Call: {call_type}",
        f"Timestamp (IST): {now.isoformat()}",
    ]
    if input_tokens is not None and output_tokens is not None:
        lines.append(f"Tokens: input={input_tokens}, output={output_tokens}, total={input_tokens + output_tokens}")
    lines.extend(
        [
            "",
            "--- Developer Prompt ---",
            developer_prompt,
            "",
            "--- User Prompt ---",
            user_prompt,
            "",
        ]
    )

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    except OSError:
        pass
