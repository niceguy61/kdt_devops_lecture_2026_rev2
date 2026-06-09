CREATE TABLE IF NOT EXISTS service_bootstrap (
    id serial PRIMARY KEY,
    service_name text NOT NULL,
    created_at timestamptz DEFAULT now()
);

INSERT INTO service_bootstrap(service_name)
VALUES ('week3-msa-demo')
ON CONFLICT DO NOTHING;
