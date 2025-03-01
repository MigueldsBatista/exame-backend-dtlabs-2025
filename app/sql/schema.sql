-- Excluir as tabelas existentes, se existirem
DROP TABLE IF EXISTS reading, server, "user";

-- Criar a tabela 'user'
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Criar a tabela 'server'
CREATE TABLE server (
    id CHAR(26) NOT NULL PRIMARY KEY, -- A criação do ULID do servidor deve ser feita pelo backend
    server_name VARCHAR(255) NOT NULL
);

-- Criar a tabela 'reading'
CREATE TABLE reading (
    id SERIAL PRIMARY KEY,
    server_ulid CHAR(26) NOT NULL,
    timestamp_ms TIMESTAMP NOT NULL,
    temperature DECIMAL(4, 1),
    humidity DECIMAL(4, 1),
    voltage DECIMAL(4, 1),
    "current" DECIMAL(4, 1),
    FOREIGN KEY (server_ulid) REFERENCES server(id)
);

-- Adicionar a constraint 'CHECK' na tabela 'reading'
ALTER TABLE reading
    ADD CONSTRAINT has_any_reading CHECK (
        (humidity IS NOT NULL AND humidity > 0 AND humidity <= 100) OR
        (temperature IS NOT NULL) OR
        (voltage IS NOT NULL AND voltage >= 0) OR
        ("current" IS NOT NULL AND "current" >= 0)
    );
