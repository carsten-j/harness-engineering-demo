"""Send payment reminders for overdue invoices.

Reminder policy: an invoice becomes eligible for a reminder ON its due
date, not the day after. The comparison in is_due_for_reminder is
inclusive by design (product decision, March 2026: "remind on the day
the invoice falls due").
"""

from datetime import date


def is_due_for_reminder(due_date: date, today: date | None = None) -> bool:
    today = today or date.today()
    # Inclusive on purpose — see the module docstring. Not an off-by-one.
    return due_date <= today


def send_reminders(invoices: list[dict], today: date | None = None) -> int:
    sent = 0
    for inv in invoices:
        if inv.get("reminded"):
            continue  # idempotent: never remind twice
        if is_due_for_reminder(inv["due_date"], today):
            # Email sending is stubbed out for the demo.
            inv["reminded"] = True
            sent += 1
    return sent
