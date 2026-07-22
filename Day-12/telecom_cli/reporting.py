"""Reporting helpers for aggregate billing and anomalies."""
import logging
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .fraud import is_suspicious
from .models import CdrRecord
from .rating import compute_cost

logger = logging.getLogger(__name__)


def build_report(
    subscribers: dict[str, Any],
    cdr_records: list[CdrRecord],
    fraud_duration_threshold_sec: int,
) -> dict[str, Any]:
    """Build the final JSON-compatible daily report structure."""
    subscriber_totals: dict[str, dict[str, Any]] = {}
    anomalies: list[dict[str, Any]] = []
    unknown_msisdns: set[str] = set()

    for cdr in cdr_records:
        cost = cdr.compute_cost()
        suspicious = cdr.is_suspicious(fraud_duration_threshold_sec)

        if cdr.msisdn not in subscribers:
            unknown_msisdns.add(cdr.msisdn)
            anomalies.append(
                {
                    "type": "unknown_subscriber",
                    "msisdn": cdr.msisdn,
                    "call_type": cdr.call_type,
                    "duration_sec": cdr.duration_sec,
                    "cost": cost,
                    "suspicious": suspicious,
                }
            )
            continue

        subscriber = subscribers[cdr.msisdn]
        subscriber.add_call(cdr)

        totals = subscriber_totals.setdefault(
            cdr.msisdn,
            {
                "msisdn": cdr.msisdn,
                "plan_type": subscriber.plan_type,
                "total_calls": 0,
                "total_cost": 0.0,
                "suspicious_calls": 0,
            },
        )

        totals["total_calls"] += 1
        totals["total_cost"] = round(totals["total_cost"] + cost, 2)
        if suspicious:
            totals["suspicious_calls"] += 1

    return {
        "summary": {
            "subscriber_count": len(subscriber_totals),
            "cdr_count": len(cdr_records),
            "anomaly_count": len(anomalies),
            "unknown_subscriber_count": len(unknown_msisdns),
        },
        "subscribers": list(subscriber_totals.values()),
        "anomalies": anomalies,
    }


def print_console_summary(report: dict[str, Any]) -> None:
    """Print a human-readable summary of the report."""
    logger.info("Daily Billing Summary")
    print("--- Daily Billing Summary ---")
    print(f"Subscribers processed: {report['summary']['subscriber_count']}")
    print(f"Total CDRs evaluated: {report['summary']['cdr_count']}")
    print(f"Anomalies detected: {report['summary']['anomaly_count']}")
    print("")

    for subscriber in report["subscribers"]:
        print(
            f"{subscriber['msisdn']}: {subscriber['total_calls']} calls, "
            f"${subscriber['total_cost']:.2f}, "
            f"{subscriber['suspicious_calls']} suspicious"
        )

    if report["anomalies"]:
        print("\nUnknown subscriber anomalies:")
        for anomaly in report["anomalies"]:
            print(
                f"  {anomaly['msisdn']} ({anomaly['call_type']}, "
                f"{anomaly['duration_sec']}s) suspicious={anomaly['suspicious']}"
            )
