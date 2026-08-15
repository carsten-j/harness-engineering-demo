-- 0001: initial schema. Applied migrations are immutable — add a new
-- numbered file for any schema change.
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY,
    customer TEXT NOT NULL,
    total_cents INTEGER NOT NULL,
    due_date TEXT NOT NULL,
    reminded INTEGER NOT NULL DEFAULT 0
);
