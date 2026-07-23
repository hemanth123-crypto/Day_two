"""Validation helpers for raw ticket rows."""

from datetime import datetime
from typing import Optional

from .config import VALID_PRIORITIES


def validate_row(row: dict) -> tuple[bool, Optional[str]]:
    """Validate a CSV row and return a success flag plus a reason string.

    Parameters:
        row: A dictionary containing CSV column values.

    Returns:
        A tuple of ``(is_valid, reason)`` where ``reason`` is ``None`` for
        valid rows and a descriptive message for invalid rows.
    """
    reasons = []

    ticket_id = (row.get("ticket_id") or "").strip()
    customer_name = (row.get("customer_name") or "").strip()
    priority_raw = (row.get("priority_raw") or "").strip().lower()
    created_at = (row.get("created_at") or "").strip()
    sla_hours_value = (row.get("sla_hours") or "").strip()

    if not ticket_id:
        reasons.append("missing ticket_id")
    if not customer_name:
        reasons.append("missing customer_name")

    try:
        sla_hours = float(sla_hours_value)
    except (TypeError, ValueError):
        sla_hours = None

    if sla_hours is None or sla_hours <= 0:
        reasons.append("invalid sla_hours")

    try:
        datetime.fromisoformat(created_at.replace(" ", "T"))
    except ValueError:
        reasons.append("invalid created_at")

    if priority_raw not in VALID_PRIORITIES:
        reasons.append("invalid priority_raw")

    if reasons:
        return False, "; ".join(reasons)

    return True, None


def normalize_row(row: dict) -> dict:
    """Trim whitespace from all string values in a row."""
    return {key: (value.strip() if isinstance(value, str) else value) for key, value in row.items()}
