-- 0002: add paid_at to invoices. NULL means the invoice is unpaid.
ALTER TABLE invoices ADD COLUMN paid_at TEXT;
