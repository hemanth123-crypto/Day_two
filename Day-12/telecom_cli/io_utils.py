"""I/O helpers for loading subscribers, CDRs, and writing reports."""
import csv
import json
import logging
from pathlib import Path
from typing import Any, Iterable

from .config import ALLOWED_CALL_TYPES
from .models import CdrRecord, Subscriber

logger = logging.getLogger(__name__)


def load_subscribers(path: Path) -> dict[str, Subscriber]:
    """Load a subscriber master list from JSON.

    Args:
        path: Path to the JSON contacts file.

    Returns:
        A mapping of msisdn to Subscriber.
    """
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    subscribers: dict[str, Subscriber] = {}
    for item in data:
        if not isinstance(item, dict):
            logger.warning("Skipping invalid subscriber entry: %r", item)
            continue

        msisdn = item.get("msisdn")
        plan_type = item.get("plan_type")
        if not msisdn or not plan_type:
            logger.warning("Skipping incomplete subscriber entry: %r", item)
            continue

        subscribers[msisdn] = Subscriber(msisdn=msisdn, plan_type=plan_type)

    return subscribers


def parse_cdr_line(row: dict[str, str]) -> CdrRecord:
    """Parse and validate a single CSV CDR row.

    Args:
        row: Raw row from csv.DictReader.

    Returns:
        Parsed CdrRecord.

    Raises:
        ValueError: If a required field is missing or malformed.
    """
    msisdn = row.get("msisdn")
    call_type = row.get("call_type")
    duration_raw = row.get("duration_sec")

    if not msisdn:
        raise ValueError("msisdn is required")
    if not call_type:
        raise ValueError("call_type is required")
    if not duration_raw:
        raise ValueError("duration_sec is required")

    if call_type not in ALLOWED_CALL_TYPES:
        raise ValueError(f"Unsupported call_type: {call_type}")

    try:
        duration_sec = int(duration_raw)
    except ValueError as exc:
        raise ValueError(f"Invalid duration_sec value: {duration_raw}") from exc

    return CdrRecord(msisdn=msisdn, call_type=call_type, duration_sec=duration_sec)


def parse_legacy_line(line: str) -> dict[str, str]:
    """Parse a legacy pipe-delimited CDR line into a normalized row dict."""
    parts = [segment.strip() for segment in line.split("|")]
    if len(parts) != 3:
        raise ValueError(f"Legacy line must contain 3 fields: {line}")

    return {"msisdn": parts[0], "call_type": parts[1], "duration_sec": parts[2]}


def load_cdrs(path: Path) -> tuple[Iterable[CdrRecord], int, int]:
    """Load CDR records from a CSV file, count malformed rows.

    Args:
        path: Path to the CSV file.

    Returns:
        A tuple of (records, total_rows, malformed_count).
    """
    records: list[CdrRecord] = []
    malformed_count = 0
    total_rows = 0

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            total_rows += 1
            try:
                record = parse_cdr_line(row)
            except ValueError as exc:
                logger.warning("Skipping malformed CDR row %d: %s", total_rows, exc)
                malformed_count += 1
            else:
                records.append(record)

    return records, total_rows, malformed_count


def write_report(path: Path, report: Any) -> None:
    """Write a JSON report to disk."""
    with path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
