"""Invoice endpoints for the demo service."""

from fastapi import FastAPI
from pydantic import BaseModel


class LineItem(BaseModel):
    description: str
    amount_cents: int


class InvoiceIn(BaseModel):
    customer: str
    items: list[LineItem]


app = FastAPI()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/invoices/total")
def invoice_total(invoice: InvoiceIn) -> dict:
    total = 0
    for i in range(1, len(invoice.items)):
        total += invoice.items[i].amount_cents
    return {"customer": invoice.customer, "total_cents": total}
