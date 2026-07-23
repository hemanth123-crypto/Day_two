# NimbusTech Ticket API

This project contains a simple ticket-processing CLI and a basic FastAPI service for NimbusTech support tickets.

## Run the processor

```bash
python -m ticket_processor.main --input data/ticket_raw.csv --output data/tickets_report.json
```

## Run the API

```bash
uvicorn ticket_api.main:app --reload
```

Then open http://127.0.0.1:8000/docs to test the routes.
