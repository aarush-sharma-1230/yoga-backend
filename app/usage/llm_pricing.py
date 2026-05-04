"""Per-million-token rates (USD) for LLM cost estimates; edit as pricing changes."""

INPUT_USD_PER_MILLION_TOKENS = 1.0
OUTPUT_USD_PER_MILLION_TOKENS = 1.0
REASONING_USD_PER_MILLION_TOKENS = 1.0


def config_usd_to_micro_usd(usd: float) -> int:
    """Convert a configured dollar cap (e.g. env) to integer micro-USD for comparisons and storage."""
    return int(round(float(usd) * 1_000_000))
