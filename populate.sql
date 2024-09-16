\c zupit_db

SELECT create_brazilian(
    'Antonio',
    'a@a.com',
    '123',
    '1990-05-15',
    'MAN',
    '12345678901'
);

SELECT create_foreigner(
    'Maria Gonzalez',
    'maria@example.com',
    'senha456',
    '1985-09-10',
    'WOMAN',
    'A1234567'
);

SELECT create_driver(
    1,
    '98765432100',
    'Prefere não fumar no carro'
);

SELECT create_car(
    '00123456789',
    1,
    'Toyota',
    'Corolla',
    'XYZ1234',
    'Preto'
);

SELECT create_address(
    '12345-678',
    'Rua Principal',
    'Cidade Exemplo',
    'EX',
    'Bairro Central',
    '10',
    'PICK_UP',
    1
);

SELECT create_address(
    '23456-789',
    'Avenida Secundária',
    'Cidade Intermediária',
    'EX',
    'Bairro Intermediário',
    '25',
    'MIDDLE',
    1
);

SELECT create_address(
    '34567-890',
    'Rua Final',
    'Cidade Destino',
    'EX',
    'Bairro Final',
    '30',
    'PICK_OFF',
    1
);

SELECT create_travel(
    1,
    '00123456789',
    2,
    '2024-09-15 08:00:00+00',
    (SELECT id FROM address WHERE cep = '12345-678'),
    (SELECT id FROM address WHERE cep = '23456-789'),
    3600,
    '10km',
    (SELECT id FROM address WHERE cep = '34567-890'),
    1800,
    '20km'
);

SELECT confirm_travel(
    2,
    1
);

