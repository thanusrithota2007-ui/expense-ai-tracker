-- Apply this migration to Supabase before deploying the updated application.
-- It only adds a table; it does not alter or delete existing expenses.
CREATE TABLE IF NOT EXISTS public.processed_messages (
    message_id VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Do not create anon/authenticated policies. The application uses its backend
-- Postgres connection; the runtime DB role must own this table or have BYPASSRLS.
ALTER TABLE public.processed_messages ENABLE ROW LEVEL SECURITY;
