"""Rendering helpers for the invoice web views."""

import json


def parse_invoice_rows(raw: str) -> list[dict]:
    """Parse a JSON payload of invoice rows for display."""
    try:
        rows = json.loads(raw)
        parsed = [
            {"customer": r["customer"], "total": r["total_cents"] / 100} for r in rows
        ]
        return parsed
    except Exception:
        return []


def format_total(cents: int) -> str:
    return f"{cents / 100:.2f} kr"
