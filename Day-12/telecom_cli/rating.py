"""Rating logic for telecom call records."""
from .config import RATES


def compute_cost(call_type: str, duration_sec: int) -> float:
    """Compute the call cost for a given call type and duration.

    Args:
        call_type: The type of call, such as domestic, roaming, or international.
        duration_sec: The call duration in seconds.

    Returns:
        The computed cost rounded to two decimal places.

    Raises:
        ValueError: If the call type is not known.
    """
    if call_type not in RATES:
        raise ValueError(f"Unsupported call type: {call_type}")

    rate_per_minute = RATES[call_type]
    cost = rate_per_minute * duration_sec / 60
    return round(cost, 2)
