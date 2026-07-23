"""Process raw ticket exports into a structured JSON report."""

import csv
import json
import logging
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .config import (
    DEFAULT_INPUT_PATH,
    DEFAULT_OUTPUT_PATH,
    INVALID_ROW_ABORT_RATIO,
    REQUIRED_COLUMNS,
    VALID_PRIORITIES,
)
from .models import InvalidRow, TicketRecord
from .validators import normalize_row, validate_row

logger = logging.getLogger(__name__)


def _parse_created_at(value: str) -> datetime:
    """Parse a created-at timestamp from CSV input."""
    return datetime.fromisoformat(value.replace(" ", "T"))


def _build_ticket_record(row: dict) -> TicketRecord:
    """Translate a validated row into a ticket dataclass."""
    created_at_value = _parse_created_at(row["created_at"])
    sla_hours = float(row["sla_hours"])
    priority_raw = row["priority_raw"].lower()
    priority_score = VALID_PRIORITIES[priority_raw]
    status = row["status"].strip().lower()
    deadline = created_at_value + timedelta(hours=sla_hours)
    sla_breached = deadline < datetime.now() and status != "closed"

    return TicketRecord(
        ticket_id=row["ticket_id"].strip(),
        customer_name=row["customer_name"].strip(),
        category=row["category"].strip().lower(),
        priority_raw=priority_raw,
        priority_score=priority_score,
        created_at=created_at_value.strftime("%Y-%m-%dT%H:%M:%S"),
        sla_hours=sla_hours,
        status=status,
        sla_breached=sla_breached,
    )


def _build_raw_row(row: dict) -> str:
    """Create a pipe-separated raw row string for invalid-row reporting."""
    return ",".join(str(row.get(column, "")) for column in sorted(REQUIRED_COLUMNS))


def process_tickets(input_path: Path = DEFAULT_INPUT_PATH) -> dict[str, Any] | None:
    """Read, validate, classify and summarize ticket rows.

    Parameters:
        input_path: Path to the raw CSV file.

    Returns:
        A report dictionary, or ``None`` if the input is invalid beyond the
        allowed threshold.
    """
    logger.info("Starting ticket processing for %s", input_path)

    if not input_path.exists():
        logger.error("Input file not found: %s", input_path)
        return None

    with input_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            logger.error("Input CSV is missing a header row")
            return None

        missing_columns = REQUIRED_COLUMNS.difference(set(reader.fieldnames))
        if missing_columns:
            logger.error("Input CSV is missing required columns: %s", ", ".join(sorted(missing_columns)))
            return None

        rows = [normalize_row(row) for row in reader]

    if not rows:
        logger.error("Input CSV is empty")
        return None

    valid_tickets = []
    invalid_rows = []

    for row in rows:
        is_valid, reason = validate_row(row)
        if not is_valid:
            invalid_rows.append(InvalidRow(raw_row=_build_raw_row(row), reason=reason or "invalid row").to_dict())
            continue
        valid_tickets.append(_build_ticket_record(row).to_dict())

    logger.info("Processed %s rows; %s valid and %s invalid", len(rows), len(valid_tickets), len(invalid_rows))

    invalid_ratio = len(invalid_rows) / len(rows)
    if invalid_ratio > INVALID_ROW_ABORT_RATIO:
        logger.error(
            "Abort triggered: invalid-row ratio %.2f exceeds %.2f",
            invalid_ratio,
            INVALID_ROW_ABORT_RATIO,
        )
        return None

    category_counts = Counter(ticket["category"] for ticket in valid_tickets)
    breached_count = sum(1 for ticket in valid_tickets if ticket["sla_breached"])

    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "summary": {
            "total_rows": len(rows),
            "valid_tickets": len(valid_tickets),
            "invalid_rows": len(invalid_rows),
            "breached_count": breached_count,
            "by_category": dict(sorted(category_counts.items())),
        },
        "tickets": valid_tickets,
        "invalid_rows": invalid_rows,
    }

    logger.info("Report prepared successfully")
    return report


def write_report(report: dict[str, Any], output_path: Path = DEFAULT_OUTPUT_PATH) -> None:
    """Write a report dictionary to disk as JSON."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
    logger.info("Report written to %s", output_path)


def main() -> int:
    """Run the processor from the command line."""
    import argparse

    parser = argparse.ArgumentParser(description="Process raw NimbusTech tickets")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH, help="Path to the raw CSV file")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH, help="Path to the output JSON report")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")

    try:
        report = process_tickets(args.input)
    except (FileNotFoundError, ValueError, csv.Error) as exc:
        logger.error("Processing failed: %s", exc)
        return 1

    if report is None:
        return 1

    write_report(report, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
