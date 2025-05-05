INSERT INTO users
(email, login, password_hash, "role", first_name, last_name, birthdate)
VALUES('admin@example.com', 'admin', '$pbkdf2-sha256$29000$PifkHEOIcW5NaY0xprQ2Jg$ta5FyWlaiyJo26jrNcdTE2tMFSQim5mbgH1oF1LhPa0', 'Администратор', NULL, NULL, NULL);