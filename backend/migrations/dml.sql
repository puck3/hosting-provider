INSERT INTO users (
        email,
        login,
        password_hash,
        "role",
        first_name,
        last_name,
        birthdate
    )
VALUES(
        'admin@example.com',
        'admin',
        '$2b$12$iTmo8adUrhGIMEGcsvm.wOOu2X/H9LP/ah3xW/qO1tSurlrQCJqqK',
        'admin',
        NULL,
        NULL,
        NULL
    );