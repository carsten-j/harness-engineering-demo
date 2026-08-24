-- 0002: record when an invoice was paid. NULL means unpaid.
ALTER TABLE invoices ADD COLUMN paid_at TEXT;
