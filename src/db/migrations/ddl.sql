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
    frequency DECIMAL(5, 2) NOT NULL CHECK (frequency > 0),
    socket VARCHAR(50) NOT NULL
);

CREATE TABLE gpus (
    gpu_id SERIAL PRIMARY KEY,
    gpu_name VARCHAR(50) NOT NULL,
    gpu_vendor VARCHAR(50) NOT NULL,
    vram_type VARCHAR(50) NOT NULL,
    vram_gb INTEGER NOT NULL CHECK (vram_gb > 0)
);

CREATE TABLE hardware_configurations (
    hardware_configuration_id SERIAL PRIMARY KEY,
    cpu_id INTEGER NOT NULL REFERENCES cpus ON DELETE CASCADE,
    cpus_count INTEGER DEFAULT 1 CHECK (cpus_count > 0),
    gpu_id INTEGER NOT NULL REFERENCES gpus ON DELETE CASCADE,
    gpus_count INTEGER DEFAULT 0 CHECK (gpus_count >= 0),
    storage_gb INTEGER NOT NULL CHECK (storage_gb > 0),
    ram_gb INTEGER NOT NULL CHECK (ram_gb > 0),
    bandwidth_mbps INTEGER NOT NULL CHECK (bandwidth_mbps > 0)
);

CREATE TABLE operating_systems (
    operating_system_id SERIAL PRIMARY KEY,
    operating_system_name VARCHAR(50),
    operating_system_version VARCHAR(50)
);

CREATE TYPE status_type AS ENUM ('active', 'inactive', 'maintenance', 'decommissioned');

CREATE TABLE servers (
    server_id SERIAL PRIMARY KEY,
    status status_type NOT NULL,
    datacenter_id INTEGER NOT NULL REFERENCES datacenters ON DELETE CASCADE,
    hardware_configuration_id INTEGER NOT NULL REFERENCES hardware_configurations ON DELETE CASCADE,
    operating_system_id INTEGER REFERENCES operating_systems ON DELETE RESTRICT
);

CREATE TABLE ip_addresses (
    ip_address_id SERIAL PRIMARY KEY,
    ip_address inet NOT NULL UNIQUE,
    server_id INTEGER REFERENCES servers ON DELETE CASCADE
);

CREATE TYPE billing_period_type AS ENUM('hourly', 'daily', 'monthly');

CREATE TABLE plans (
    plan_id SERIAL PRIMARY KEY,
    hardware_configuration_id INTEGER NOT NULL REFERENCES hardware_configurations ON DELETE CASCADE,
    price DECIMAL(10, 2) NOT NULL,
    billing_period billing_period_type NOT NULL,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    UNIQUE (hardware_configuration_id, billing_period)
);

CREATE TABLE rentals (
    rental_id SERIAL PRIMARY KEY,
    server_id INTEGER NOT NULL REFERENCES servers ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users ON DELETE CASCADE,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    billing_period billing_period_type NOT NULL,
    start_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_at TIMESTAMP NOT NULL CHECK (end_at > start_at)
);

CREATE TYPE action_type AS ENUM ('create', 'update', 'delete');

CREATE TYPE entity_type AS ENUM ('server', 'rental', 'backup');

CREATE TABLE backups (
    backup_id SERIAL PRIMARY KEY,   
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(user_id) ON DELETE RESTRICT,
    filename VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE action_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users ON DELETE CASCADE,
    action action_type NOT NULL,
    entity_id INTEGER NOT NULL,
    entity entity_type NOT NULL,
    description TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
