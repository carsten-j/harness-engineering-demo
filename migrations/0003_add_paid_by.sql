-- 0003: add paid_by to invoices. NULL means the invoice is unpaid.
ALTER TABLE invoices ADD COLUMN paid_by TEXT;
