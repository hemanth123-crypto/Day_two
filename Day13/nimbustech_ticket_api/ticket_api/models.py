"""Pydantic models for the NimbusTech ticket API."""

from pydantic import BaseModel, Field


class TicketBase(BaseModel):
    """Core fields for a ticket response or creation request."""

    ticket_id: str = Field(..., min_length=1)
    customer_name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    priority_raw: str = Field(..., min_length=1)
    created_at: str = Field(..., min_length=1)
    sla_hours: float = Field(..., gt=0)
    status: str = Field(..., min_length=1)


class TicketCreate(TicketBase):
    """Request model for creating a new ticket."""


class TicketUpdate(BaseModel):
    """Request model for updating ticket status or priority."""

    status: str | None = None
    priority_raw: str | None = None
