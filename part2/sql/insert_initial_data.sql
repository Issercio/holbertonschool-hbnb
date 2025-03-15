-- Insertion de l'administrateur avec remplacement si existe déjà
INSERT OR REPLACE INTO users (id, email, first_name, last_name, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$tXu7Tw1JsYX6wYhTzRTQb.zEYzO.bAm6PrnG4F7.X.1TFAhCZXIHe',
    TRUE
);

-- Insertion des commodités en ignorant les doublons
INSERT OR IGNORE INTO amenities (id, name) VALUES
    ('f268d3f2-0f84-4f86-bd4f-9f8e6c8f0c9a', 'WiFi'),
    ('a3e0f1b1-5d8c-4e6b-9e7d-2c9f8b0d1a3e', 'Swimming Pool'),
    ('c7d6e5f4-3b2a-1c9d-8e7f-6a5b4c3d2e1f', 'Air Conditioning');
