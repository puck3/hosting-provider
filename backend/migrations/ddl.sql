CREATE TYPE role_type AS ENUM ('user', 'admin');
CREATE TABLE IF NOT EXISTS users(
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    login VARCHAR(50) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role role_type DEFAULT 'user',
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birthdate DATE
);
CREATE TABLE IF NOT EXISTS datacenters(
    datacenter_id SERIAL PRIMARY KEY,
    datacenter_name VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS cpus(
    cpu_id SERIAL PRIMARY KEY,
    cpu_name VARCHAR(50) NOT NULL,
    cpu_vendor VARCHAR(50) NOT NULL,
    cores INTEGER NOT NULL CHECK (cores > 0),
    frequency DECIMAL(5, 2) NOT NULL CHECK (frequency > 0)
);
CREATE TABLE IF NOT EXISTS gpus(
    gpu_id SERIAL PRIMARY KEY,
    gpu_name VARCHAR(50) NOT NULL,
    gpu_vendor VARCHAR(50) NOT NULL,
    vram_type VARCHAR(50) NOT NULL,
    vram_gb INTEGER NOT NULL CHECK (vram_gb > 0)
);
CREATE TABLE IF NOT EXISTS hardwares(
    hardware_id SERIAL PRIMARY KEY,
    cpu_id INTEGER NOT NULL REFERENCES cpus ON DELETE CASCADE,
    cpus_count INTEGER DEFAULT 1 CHECK (cpus_count > 0),
    gpu_id INTEGER REFERENCES gpus ON DELETE CASCADE,
    gpus_count INTEGER DEFAULT 0 CHECK (gpus_count >= 0),
    storage_tb INTEGER NOT NULL CHECK (storage_tb > 0),
    ram_gb INTEGER NOT NULL CHECK (ram_gb > 0),
    bandwidth_gbps INTEGER NOT NULL CHECK (bandwidth_gbps > 0),
    UNIQUE (
        cpu_id,
        cpus_count,
        gpu_id,
        gpus_count,
        storage_tb,
        ram_gb,
        bandwidth_gbps
    )
);
CREATE TYPE status_type AS ENUM ('rented', 'available');
CREATE TABLE IF NOT EXISTS servers(
    server_id SERIAL PRIMARY KEY,
    status status_type NOT NULL,
    datacenter_id INTEGER NOT NULL REFERENCES datacenters ON DELETE CASCADE,
    hardware_id INTEGER NOT NULL REFERENCES hardwares ON DELETE CASCADE,
    operating_system VARCHAR(50)
);
CREATE TYPE billing_period_type AS ENUM('hourly', 'daily', 'monthly');
CREATE TABLE IF NOT EXISTS plans(
    plan_id SERIAL PRIMARY KEY,
    plan_name VARCHAR(50) NOT NULL,
    hardware_id INTEGER NOT NULL REFERENCES hardwares ON DELETE CASCADE,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    billing_period billing_period_type NOT NULL,
    UNIQUE (hardware_id, billing_period)
);
CREATE TABLE IF NOT EXISTS rentals(
    rental_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users ON DELETE CASCADE,
    server_id INTEGER NOT NULL REFERENCES servers ON DELETE RESTRICT,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    billing_period billing_period_type NOT NULL,
    start_at TIMESTAMP NOT NULL,
    end_at TIMESTAMP NOT NULL CHECK (end_at > start_at),
    update_at TIMESTAMP NOT NULL
);
CREATE OR REPLACE FUNCTION set_update_at() RETURNS TRIGGER AS $$ BEGIN NEW.update_at = CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow';
return NEW;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER update_rentals BEFORE
UPDATE ON rentals FOR EACH ROW EXECUTE FUNCTION set_update_at();
CREATE VIEW extended_hardwares AS (
    SELECT h.hardware_id,
        c.cpu_id,
        c.cpu_name,
        c.cpu_vendor,
        c.cores,
        c.frequency,
        h.cpus_count,
        g.gpu_id,
        g.gpu_name,
        g.gpu_vendor,
        g.vram_type,
        g.vram_gb,
        h.gpus_count,
        h.storage_tb,
        h.ram_gb,
        h.bandwidth_gbps
    FROM hardwares h
        LEFT JOIN cpus c using (cpu_id)
        LEFT JOIN gpus g using (gpu_id)
);
--CREATE VIEW extended_servers AS (
--    SELECT 
--        *
--    FROM 
--        servers
--        LEFT JOIN datacenters USING (datacenter_id)
--        LEFT JOIN extended_hardwares USING (hardware_id)
--);
--CREATE VIEW extended_rentals AS (
--    SELECT 
--        *
--    FROM 
--        rentals
--        LEFT JOIN users USING (user_id)
--        LEFT JOIN extended_servers USING (server_id)
--);
CREATE VIEW available_plans_with_countries AS (
    WITH countries AS (
        SELECT d.country,
            s.hardware_id
        FROM servers s
            LEFT JOIN datacenters d USING (datacenter_id)
        WHERE s.status = 'available'
        GROUP BY d.country,
            s.hardware_id
    )
    SELECT p.plan_id,
        p.plan_name,
        p.price,
        p.billing_period,
        c.country,
        h.hardware_id,
        h.cpu_id,
        h.cpu_name,
        h.cpu_vendor,
        h.cores,
        h.frequency,
        h.cpus_count,
        h.gpu_id,
        h.gpu_name,
        h.gpu_vendor,
        h.vram_type,
        h.vram_gb,
        h.gpus_count,
        h.storage_tb,
        h.ram_gb,
        h.bandwidth_gbps
    FROM plans p
        JOIN countries c USING (hardware_id)
        LEFT JOIN extended_hardwares h USING (hardware_id)
);