"""In-memory ticket store for the NimbusTech MVP API."""

import json
from pathlib import Path
from typing import Any

from ticket_processor.config import DEFAULT_OUTPUT_PATH, VALID_PRIORITIES


class TicketStore:
    """Load the processed report into memory and expose CRUD helpers."""

    def __init__(self, tickets: list[dict[str, Any]] | None = None) -> None:
        """Initialise the store with a list of ticket dictionaries."""
        self._tickets = tickets or []

    @classmethod
    def from_report(cls, report_path: Path | None = None) -> "TicketStore":
        """Load the ticket list from a JSON report file."""
        path = report_path or DEFAULT_OUTPUT_PATH
        if not path.exists():
            return cls([])

        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)

        tickets = payload.get("tickets", [])
        return cls(tickets)

    def list_tickets(self) -> list[dict[str, Any]]:
        """Return the full list of tickets."""
        return list(self._tickets)

    def list_breached(self) -> list[dict[str, Any]]:
        """Return tickets whose SLA has been breached."""
        return [ticket for ticket in self._tickets if ticket.get("sla_breached")]

    def get_ticket(self, ticket_id: str) -> dict[str, Any] | None:
        """Return one ticket by id, or ``None`` if it does not exist."""
        for ticket in self._tickets:
            if ticket.get("ticket_id") == ticket_id:
                return ticket
        return None

    def create_ticket(self, ticket: dict[str, Any]) -> dict[str, Any]:
        """Add a new ticket and return the created record."""
        priority_raw = str(ticket.get("priority_raw", "")).strip().lower()
        priority_score = VALID_PRIORITIES.get(priority_raw, 1)
        ticket.setdefault("priority_score", priority_score)
        ticket.setdefault("sla_breached", False)
        self._tickets.append(ticket)
        return ticket

    def update_ticket(self, ticket_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        """Update an existing ticket's mutable fields."""
        for ticket in self._tickets:
            if ticket.get("ticket_id") == ticket_id:
                ticket.update(updates)
                return ticket
        return None

    def delete_ticket(self, ticket_id: str) -> bool:
        """Remove a ticket by id and return whether it was deleted."""
        for index, ticket in enumerate(self._tickets):
            if ticket.get("ticket_id") == ticket_id:
                del self._tickets[index]
                return True
        return False
