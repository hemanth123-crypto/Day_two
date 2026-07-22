"""CLI entry point for the Telecom CDR & Billing Insights tool."""
import argparse
import logging
import sys
from datetime import date
from pathlib import Path

from .config import DEFAULT_FRAUD_DURATION_THRESHOLD_SEC, MAX_MALFORMED_RATIO
from .io_utils import load_cdrs, load_subscribers, write_report
from .reporting import build_report, print_console_summary


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


def print_startup_banner() -> None:
    print(f"Telecom CDR & Billing Insights CLI started on {date.today().isoformat()}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Telecom CDR & Billing Insights CLI",
    )
    parser.add_argument(
        "--subscribers",
        required=True,
        help="Path to subscribers JSON file",
    )
    parser.add_argument(
        "--cdrs",
        required=True,
        help="Path to CDR CSV file",
    )
    parser.add_argument(
        "--output-report",
        required=True,
        help="Path to write the daily report JSON file",
    )
    parser.add_argument(
        "--fraud-duration-threshold",
        type=int,
        default=DEFAULT_FRAUD_DURATION_THRESHOLD_SEC,
        help="Max international call duration in seconds before flagging as suspicious",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    configure_logging()
    print_startup_banner()
    args = parse_args(argv)

    subscribers = load_subscribers(Path(args.subscribers))
    cdr_records, total_rows, malformed_count = load_cdrs(Path(args.cdrs))

    malformed_ratio = malformed_count / total_rows if total_rows else 0.0
    if malformed_ratio > MAX_MALFORMED_RATIO:
        logging.critical(
            "Too many malformed CDR rows: %d of %d (%.1f%%). Exiting without writing report.",
            malformed_count,
            total_rows,
            malformed_ratio * 100,
        )
        return 1

    report = build_report(
        subscribers=subscribers,
        cdr_records=list(cdr_records),
        fraud_duration_threshold_sec=args.fraud_duration_threshold,
    )

    write_report(Path(args.output_report), report)
    print_console_summary(report)

    logging.info("Report written to %s", args.output_report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
