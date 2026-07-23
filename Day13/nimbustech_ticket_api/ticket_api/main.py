"""Basic FastAPI service for NimbusTech ticket operations."""

from fastapi import FastAPI, HTTPException
from pathlib import Path

from ticket_processor.config import DEFAULT_OUTPUT_PATH
from .models import TicketCreate, TicketUpdate
from .store import TicketStore

app = FastAPI(title="NimbusTech Ticket Triage API")
store = TicketStore.from_report(DEFAULT_OUTPUT_PATH)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return a simple health message for the API root endpoint."""
    return {"status": "ok", "service": "ticket-triage-api"}


@app.get("/tickets")
def list_tickets() -> list[dict]:
    """Return the full list of processed tickets."""
    return store.list_tickets()


@app.get("/tickets/breached")
def list_breached_tickets() -> list[dict]:
    """Return only tickets that have breached their SLA."""
    return store.list_breached()


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str) -> dict:
    """Return one ticket by id, or raise a 404 error if it is missing."""
    ticket = store.get_ticket(ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    return ticket


@app.post("/tickets", status_code=201)
def create_ticket(payload: TicketCreate) -> dict:
    """Create a new ticket record in memory."""
    created = store.create_ticket(payload.model_dump())
    return created


@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, payload: TicketUpdate) -> dict:
    """Update an existing ticket's status and/or priority."""
    updates = {key: value for key, value in payload.model_dump(exclude_none=True).items()}
    if not updates:
        raise HTTPException(status_code=400, detail="no update fields were provided")

    ticket = store.update_ticket(ticket_id, updates)
    if ticket is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    return ticket


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: str) -> dict[str, object]:
    """Delete a ticket record from memory."""
    deleted = store.delete_ticket(ticket_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ticket not found")
    return {"deleted": True, "ticket_id": ticket_id}
