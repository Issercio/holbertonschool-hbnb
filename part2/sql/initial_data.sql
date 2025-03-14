-- Script SQL pour l'insertion des données initiales

-- Création de l'administrateur
INSERT INTO users (id, email, first_name, last_name, password, is_admin) 
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFO8y1K47YQ6mqa',  -- Hash de 'admin1234'
    TRUE
) ON DUPLICATE KEY UPDATE id=id;

-- Insertion des amenities de base
INSERT INTO amenities (id, name) VALUES
    (UUID(), 'WiFi'),
    (UUID(), 'Swimming Pool'),
    (UUID(), 'Air Conditioning')
ON DUPLICATE KEY UPDATE name=name;
