"""Configuration constants for the Telecom CDR CLI."""
from typing import Dict, Final

RATES: Final[Dict[str, float]] = {
    "domestic": 1.5,
    "roaming": 8.0,
    "international": 12.0,
}

DEFAULT_FRAUD_DURATION_THRESHOLD_SEC: Final[int] = 3600
REPORT_INDENT: Final[int] = 2
ALLOWED_CALL_TYPES: Final[frozenset[str]] = frozenset(RATES)

MAX_MALFORMED_RATIO: Final[float] = 0.1
