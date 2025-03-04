drop database exame_backend;


-- Create user table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Create server table
CREATE TABLE server (
    id CHAR(26) NOT NULL PRIMARY KEY, -- The server ULID creation should be handled by the backend
    server_name VARCHAR(255) NOT NULL
);

-- Create reading table
CREATE TABLE reading (
    id SERIAL PRIMARY KEY,
    server_ulid CHAR(26) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperature DECIMAL(4, 1),
    humidity DECIMAL(4, 1),
    voltage DECIMAL(4, 1),
    "current" DECIMAL(4, 1),
    FOREIGN KEY (server_ulid) REFERENCES server(id)
);

-- Add CHECK constraint to reading table
ALTER TABLE reading
    ADD CONSTRAINT has_any_reading CHECK (
        (humidity IS NOT NULL AND humidity > 0 AND humidity <= 100) OR
        (temperature IS NOT NULL) OR
        (voltage IS NOT NULL AND voltage >= 0) OR
        ("current" IS NOT NULL AND "current" >= 0)
    );
