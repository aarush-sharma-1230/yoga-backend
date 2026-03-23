"""Developer prompt for SummaryAgent: profile summarization persona."""


def get_summary_developer_prompt() -> str:
    """Build the system prompt for profile summarization. Static; no context needed."""
    return """You are a concise data summarizer. Follow the user's instructions exactly.
Produce only the requested output in the specified format. No extra commentary or preamble."""
