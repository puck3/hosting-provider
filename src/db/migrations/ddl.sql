CREATE TYPE role_type AS ENUM ('user', 'admin');

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    login VARCHAR(50) NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    role role_type NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birthdate DATE
);

CREATE TABLE datacenters (
    datacenter_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
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
    vram_type VARCHAR(50) NOT NULL,
    vram_gb INTEGER NOT NULL CHECK (vram_gb > 0)
);

CREATE TABLE hardware_configs (
    config_id SERIAL PRIMARY KEY,
    cpu_id INTEGER NOT NULL REFERENCES cpus ON DELETE CASCADE,
    cpus_count INTEGER DEFAULT 1 CHECK (cpus_count > 0),
    gpu_id INTEGER NOT NULL REFERENCES gpus ON DELETE CASCADE,
    gpus_count INTEGER DEFAULT 0 CHECK (gpus_count >= 0),
    storage_gb INTEGER NOT NULL CHECK (storage_gb > 0),
    ram_gb INTEGER NOT NULL CHECK (ram_gb > 0),
    bandwidth_mbps INTEGER NOT NULL CHECK (bandwidth_mbps > 0)
);

CREATE TYPE status_type AS ENUM ('active', 'inactive', 'maintenance', 'decommissioned');

CREATE TABLE servers (
    server_id SERIAL PRIMARY KEY,
    status status_type NOT NULL,
    datacenter_id INTEGER NOT NULL REFERENCES datacenters ON DELETE CASCADE,
    config_id INTEGER NOT NULL REFERENCES hardware_configs ON DELETE CASCADE,
    operating_system VARCHAR(50)
);

CREATE TYPE billing_period_type AS ENUM('hourly', 'daily', 'monthly');

CREATE TABLE plans (
    plan_id SERIAL PRIMARY KEY,
    config_id INTEGER NOT NULL REFERENCES hardware_configs ON DELETE CASCADE,
    price DECIMAL(10, 2) NOT NULL,
    billing_period billing_period_type NOT NULL,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    UNIQUE (config_id, billing_period)
);

CREATE TABLE rentals (
    rental_id SERIAL PRIMARY KEY,
    server_id INTEGER NOT NULL REFERENCES servers ON DELETE RESTRICT,
    user_id INTEGER NOT NULL REFERENCES users ON DELETE CASCADE,
    start_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_at TIMESTAMP NOT NULL CHECK (end_at > start_at)
);

CREATE TABLE backups (
    backup_id SERIAL PRIMARY KEY,   
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER NOT NULL REFERENCES users(user_id) ON DELETE RESTRICT,
    filename VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TYPE action_type AS ENUM('create', 'update', 'delete');

CREATE TABLE rental_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users ON DELETE CASCADE,
    action action_type NOT NULL,
    rental_id INTEGER NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION log_rental_actions()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO rental_logs (rental_id, action)
        VALUES (NEW.rental_id, 'create');
    
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO rental_logs (rental_id, action)
        VALUES (OLD.rental_id, 'update');

    ELSIF (TG_OP = 'DELETE') THEN
        INSERT INTO rental_logs (rental_id, action)
        VALUES (OLD.rental_id, 'delete');
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER rental_log_trigger
AFTER INSERT OR UPDATE OR DELETE ON rentals
FOR EACH ROW
EXECUTE FUNCTION log_rental_actions();

CREATE VIEW servers_overview AS (
    SELECT 
        s.server_id,
        s.status,
        dc.datacenter_id,
        dc.name AS datacenter_name,
        dc.country,
        dc.city,
        hw.config_id,
        c.cpu_name,
        c.cpu_vendor,
        c.cores,
        c.frequency,
        hw.cpus_count,
        g.gpu_name,
        g.gpu_vendor,
        g.vram_type,
        g.vram_gb,
        hw.gpus_count,
        hw.storage_gb,
        hw.ram_gb,
        hw.bandwidth_mbps,
        s.operating_system
    FROM
        servers AS s 
        JOIN datacenters AS dc ON s.datacenter_id = dc.datacenter_id
        JOIN hardware_configs AS hw ON s.config_id = hw.config_id
        JOIN cpus AS c ON hw.cpu_id = c.cpu_id
        JOIN gpus AS g ON hw.gpu_id = g.gpu_id
);
    
CREATE VIEW available_plans AS (
    WITH configs_by_datacenters AS (
        SELECT 
            dc.datacenter_id,
            s.config_id
        FROM 
            datacenters AS dc
            JOIN servers AS s USING (datacenter_id)
        WHERE s.status = 'inactive'
        GROUP BY dc.datacenter_id, s.config_id
    )
    SELECT 
        hw_dc.datacenter_id,
        dc.name AS datacenter_name,
        dc.country,
        dc.city,
        hw_dc.config_id,
        c.cpu_name,
        c.cpu_vendor,
        c.cores,
        c.frequency,
        hw.cpus_count,
        g.gpu_name,
        g.gpu_vendor,
        g.vram_type,
        g.vram_gb,
        hw.gpus_count,
        hw.storage_gb,
        hw.ram_gb,
        hw.bandwidth_mbps,
        p.plan_id,
        p.price,
        p.billing_period,
        p.name AS plan_name,
        p.description
    FROM
        configs_by_datacenters AS hw_dc
        JOIN datacenters AS dc ON hw_dc.datacenter_id = dc.datacenter_id
        JOIN hardware_configs AS hw ON hw_dc.config_id = hw.config_id 
        JOIN cpus AS c ON hw.cpu_id = c.cpu_id
        JOIN gpus AS g ON hw.gpu_id = g.gpu_id 
        JOIN plans AS p ON hw.config_id = p.config_id
);