"""Domain models for subscribers and CDR records."""
from dataclasses import dataclass, field

@dataclass
class Subscriber:
    msisdn: str
    plan_type: str
    calls: list["CdrRecord"] = field(default_factory=list)

    def add_call(self, call: "CdrRecord") -> None:
        self.calls.append(call)

    def total_cost(self) -> float:
        """Return the rounded total cost for all calls on this subscriber."""
        return round(sum(call.compute_cost() for call in self.calls), 2)

@dataclass
class CdrRecord:
    msisdn: str
    call_type: str
    duration_sec: int

    def compute_cost(self) -> float:
        """Compute the cost for this call record."""
        from .rating import compute_cost

        return compute_cost(self.call_type, self.duration_sec)

    def is_suspicious(self, international_threshold_sec: int) -> bool:
        """Determine whether this call record should be flagged as suspicious."""
        from .fraud import is_suspicious as is_suspicious_call

        return is_suspicious_call(self, self.compute_cost(), international_threshold_sec)
