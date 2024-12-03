-- Вставка данных в таблицу users
INSERT INTO users (email, login, hashed_password, role, first_name, last_name, birthdate) VALUES
('admin@example.com', 'admin', 'hashed_password_1', 'admin', 'Admin', 'User', '1980-01-01');

-- Вставка данных в таблицу datacenters
INSERT INTO datacenters (name, country, city) VALUES
('DC1', 'US', 'New York'),
('DC2', 'DE', 'Berlin'),
('DC3', 'JP', 'Tokyo');

-- Вставка данных в таблицу cpus
INSERT INTO cpus (cpu_name, cpu_vendor, cores, frequency, socket) VALUES
('Xeon E5-2680', 'Intel', 8, 2.50, 'LGA2011'),
('Ryzen 5950X', 'AMD', 16, 3.40, 'AM4'),
('Epyc 7742', 'AMD', 64, 2.25, 'SP3');

-- Вставка данных в таблицу gpus
INSERT INTO gpus (gpu_name, gpu_vendor, vram_type, vram_gb) VALUES
('RTX 3090', 'NVIDIA', 'GDDR6X', 24),
('Radeon RX 6900 XT', 'AMD', 'GDDR6', 16),
('Tesla T4', 'NVIDIA', 'GDDR6', 16);

-- Вставка данных в таблицу hardware_configurations
INSERT INTO hardware_configurations (cpu_id, cpus_count, gpu_id, gpus_count, storage_gb, ram_gb, bandwidth_mbps) VALUES
(1, 2, 1, 2, 2000, 256, 10000),
(2, 1, 2, 1, 1000, 128, 5000),
(3, 4, 3, 1, 4000, 512, 20000);

-- Вставка данных в таблицу operating_systems
INSERT INTO operating_systems (operating_system_name, operating_system_version) VALUES
('Ubuntu', '20.04'),
('Windows Server', '2019'),
('CentOS', '7');

-- Вставка данных в таблицу servers
INSERT INTO servers (status, datacenter_id, hardware_configuration_id, operating_system_id) VALUES
('inactive', 1, 1, 1),
('inactive', 2, 2, 2),
('inactive', 3, 3, 3);

-- Вставка данных в таблицу ip_addresses
INSERT INTO ip_addresses (ip_address, server_id) VALUES
('192.168.1.10', 1),
('192.168.1.11', 2),
('192.168.1.12', 3);

-- Вставка данных в таблицу plans
INSERT INTO plans (hardware_configuration_id, price, billing_period, name, description) VALUES
(1, 99.99, 'monthly', 'Standard Plan', 'Basic monthly plan with good performance'),
(2, 49.99, 'daily', 'Daily Plan', 'Pay-as-you-go daily plan'),
(3, 299.99, 'monthly', 'High Performance Plan', 'Best for intensive computing tasks');
