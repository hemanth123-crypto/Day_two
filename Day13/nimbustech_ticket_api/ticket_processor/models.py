"""Data models for the NimbusTech ticket processor."""

from dataclasses import dataclass


@dataclass
class TicketRecord:
    """Represents one validated ticket after classification."""

    ticket_id: str
    customer_name: str
    category: str
    priority_raw: str
    priority_score: int
    created_at: str
    sla_hours: float
    status: str
    sla_breached: bool

    def to_dict(self) -> dict:
        """Convert the dataclass into a JSON-serialisable dictionary."""
        return {
            "ticket_id": self.ticket_id,
            "customer_name": self.customer_name,
            "category": self.category,
            "priority_raw": self.priority_raw,
            "priority_score": self.priority_score,
            "created_at": self.created_at,
            "sla_hours": self.sla_hours,
            "status": self.status,
            "sla_breached": self.sla_breached,
        }


@dataclass
class InvalidRow:
    """Represents a row that failed validation."""

    raw_row: str
    reason: str

    def to_dict(self) -> dict:
        """Convert the dataclass into a JSON-serialisable dictionary."""
        return {"raw_row": self.raw_row, "reason": self.reason}
