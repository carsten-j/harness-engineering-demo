"""Rendering helpers for the invoice web views."""

import json
import os

def parse_invoice_rows(raw: str) -> list[dict]:
    """Parse a JSON payload of invoice rows for display."""
    try:
        rows = json.loads(raw)
        return [
            {"customer": r["customer"], "total": r["total_cents"] / 100} for r in rows
        ]
    except Exception:
        return []


def format_total(cents: int) -> str:
    return f"{cents / 100:.2f} kr"
