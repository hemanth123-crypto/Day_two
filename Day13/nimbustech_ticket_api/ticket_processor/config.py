"""Configuration constants for the NimbusTech ticket processor and API."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DEFAULT_INPUT_PATH = DATA_DIR / "ticket_raw.csv"
DEFAULT_OUTPUT_PATH = DATA_DIR / "tickets_report.json"

REQUIRED_COLUMNS = {
    "ticket_id",
    "customer_name",
    "category",
    "priority_raw",
    "created_at",
    "sla_hours",
    "status",
}

VALID_PRIORITIES = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}

INVALID_ROW_ABORT_RATIO = 0.10
"""
"""
