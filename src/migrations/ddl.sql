CREATE TYPE role_type AS ENUM ('user', 'admin');

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    login VARCHAR(50) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role role_type DEFAULT 'user',
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birthdate DATE
);

CREATE TABLE datacenters (
    datacenter_id SERIAL PRIMARY KEY,
    datacenter_name VARCHAR(50) NOT NULL,
    country VARCHAR(2) NOT NULL,
    city VARCHAR(50) NOT NULL
);

CREATE TABLE cpus (
    cpu_id SERIAL PRIMARY KEY,
    cpu_name VARCHAR(50) NOT NULL,
    cpu_vendor VARCHAR(50) NOT NULL,
    cores INTEGER NOT NULL CHECK (cores > 0),
    frequency DECIMAL(5, 2) NOT NULL CHECK (frequency > 0)
);

CREATE TABLE gpus (
    gpu_id SERIAL PRIMARY KEY,
    gpu_name VARCHAR(50) NOT NULL,
    gpu_vendor VARCHAR(50) NOT NULL,
    vram_type VARCHAR(10) NOT NULL,
    vram_gb INTEGER NOT NULL CHECK (vram_gb > 0)
);

CREATE TABLE hardwares (
    hardware_id SERIAL PRIMARY KEY,
    cpu_id INTEGER NOT NULL REFERENCES cpus ON DELETE CASCADE,
    cpus_count INTEGER DEFAULT 1 CHECK (cpus_count > 0),
    gpu_id INTEGER NOT NULL REFERENCES gpus ON DELETE CASCADE,
    gpus_count INTEGER DEFAULT 0 CHECK (gpus_count >= 0),
    storage_gb INTEGER NOT NULL CHECK (storage_gb > 0),
    ram_gb INTEGER NOT NULL CHECK (ram_gb > 0),
    bandwidth_mbps INTEGER NOT NULL CHECK (bandwidth_mbps > 0)
);

CREATE TYPE status_type AS ENUM ('active', 'inactive');

CREATE TABLE servers (
    server_id SERIAL PRIMARY KEY,
    status status_type NOT NULL,
    datacenter_id INTEGER NOT NULL REFERENCES datacenters ON DELETE CASCADE,
    hardware_id INTEGER NOT NULL REFERENCES hardwares ON DELETE CASCADE,
    operating_system VARCHAR(50)
);

CREATE TYPE billing_period_type AS ENUM('hourly', 'daily', 'monthly');

CREATE TABLE plans (
    plan_id SERIAL PRIMARY KEY,
    hardware_id INTEGER NOT NULL REFERENCES hardwares ON DELETE CASCADE,
    price DECIMAL(10, 2) NOT NULL,
    billing_period billing_period_type NOT NULL,
    plan_name VARCHAR(50) NOT NULL,
    plan_description TEXT,
    UNIQUE (hardware_id, billing_period)
);

CREATE TABLE rentals (
    rental_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users ON DELETE CASCADE,
    server_id INTEGER NOT NULL REFERENCES servers ON DELETE RESTRICT,
    plan_id INTEGER NOT NULL REFERENCES plans ON DELETE RESTRICT,
    start_at TIMESTAMP NOT NULL,
    end_at TIMESTAMP NOT NULL CHECK (end_at > start_at),
    update_at TIMESTAMP NOT NULL
);

CREATE OR REPLACE FUNCTION set_update_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_at = CURRENT_TIMESTAMP;
    return NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_rentals
BEFORE UPDATE ON rentals
FOR EACH ROW
EXECUTE FUNCTION set_update_at();

CREATE VIEW extended_hardwares AS (
    SELECT 
        *
    FROM 
        hardwares
        LEFT JOIN cpus using (cpu_id) 
        LEFT JOIN gpus using (gpu_id)
)
    
CREATE VIEW extended_servers AS (
    SELECT 
        *
    FROM 
        servers
        LEFT JOIN datacenters USING (datacenter_id)
        LEFT JOIN extended_hardwares USING (hardware_id)
)

CREATE VIEW extended_rentals AS (
    SELECT 
        *
    FROM 
        rentals
        LEFT JOIN users USING (user_id)
        LEFT JOIN extended_servers USING (server_id)
        LEFT JOIN plans USING (plan_id, hardware_id)
);

CREATE VIEW available_plans_with_countries AS (
    WITH available_hardwares_by_countries AS (
        SELECT
            country,
            hardware_id
        FROM
            servers 
            LEFT JOIN datacenters USING (datacenter_id)
        WHERE
            status = 'inactive'
        GROUP BY 
            country, hardware_id
    )
    SELECT 
        *
    FROM
        plans
        JOIN available_hardwares_by_countries USING (hardware_id)
        LEFT JOIN extended_hardwares USING (hardware_id)
);