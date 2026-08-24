-- 0003: who recorded/made the payment. NULL until the invoice is paid.
ALTER TABLE invoices ADD COLUMN paid_by TEXT;
