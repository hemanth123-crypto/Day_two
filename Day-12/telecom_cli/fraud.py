"""Fraud detection rules for telecom CDRs."""
from .models import CdrRecord


def is_suspicious(cdr: CdrRecord, cost: float, international_threshold_sec: int) -> bool:
    """Determine whether a CDR should be flagged as suspicious.

    Args:
        cdr: The parsed call detail record.
        cost: The computed cost for the CDR.
        international_threshold_sec: Maximum international call duration before flagging.

    Returns:
        True if the call is suspicious.
    """
    if cdr.duration_sec > 0 and cost == 0:
        return True

    if cdr.call_type == "international" and cdr.duration_sec > international_threshold_sec:
        return True

    return False
