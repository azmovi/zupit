\c zupit_db

-----------------------------------------------------------------
---------------------------USUARIO-------------------------------
-----------------------------------------------------------------

CREATE TYPE gender AS ENUM ('MAN', 'WOMAN');

CREATE TYPE user_public AS (
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    sex gender,
    icon BYTEA,
    doc VARCHAR
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(32) NOT NULL,
    birthday DATE NOT NULL,
    sex gender NOT NULL,
    icon BYTEA,
    user_status BOOLEAN NOT NULL
);

CREATE TABLE brazilians (
    cpf VARCHAR(11) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE foreigners (
    rnm VARCHAR(8) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE FUNCTION create_user(
    p_name VARCHAR,
    p_email VARCHAR,
    p_password VARCHAR,
    p_birthday DATE,
    p_sex gender
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_user_id INTEGER;
BEGIN
    INSERT INTO users (name, email, password, birthday, sex, icon, user_status)
    VALUES (p_name, p_email, p_password, p_birthday, p_sex, NULL, TRUE)
    RETURNING id INTO v_user_id;

    RETURN v_user_id;
END;
$$;

CREATE FUNCTION _create_brazilian(
    p_cpf VARCHAR,
    p_id_user INTEGER
) RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO brazilians (cpf, user_id)
    VALUES (p_cpf, p_id_user);
END;
$$;

CREATE FUNCTION create_brazilian(
    p_name VARCHAR,
    p_email VARCHAR,
    p_password VARCHAR,
    p_birthday DATE,
    p_sex gender,
    p_cpf VARCHAR
) RETURNS SETOF user_public
LANGUAGE plpgsql
AS $$
DECLARE 
    v_user_id INTEGER;
BEGIN
    v_user_id := create_user(p_name, p_email, p_password, p_birthday, p_sex);
    PERFORM _create_brazilian(p_cpf, v_user_id);

    RETURN QUERY 
    SELECT v_user_id, p_name, p_email, p_birthday, p_sex, NULL::BYTEA, p_cpf;
END;
$$;

CREATE FUNCTION _create_foreigner(
    p_rnm VARCHAR,
    p_id_user INTEGER
) RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO foreigners (rnm, user_id)
    VALUES (p_rnm, p_id_user);
END;
$$;

CREATE FUNCTION create_foreigner(
    p_name VARCHAR,
    p_email VARCHAR,
    p_password VARCHAR,
    p_birthday DATE,
    p_sex gender,
    p_rnm VARCHAR
) RETURNS SETOF user_public
LANGUAGE plpgsql
AS $$
DECLARE 
    v_user_id INTEGER;
BEGIN
    v_user_id := create_user(p_name, p_email, p_password, p_birthday, p_sex);
    PERFORM _create_foreigner(p_rnm, v_user_id);

    RETURN QUERY
    SELECT v_user_id, p_name, p_email, p_birthday, p_sex, NULL::BYTEA, p_rnm;
END;
$$;

CREATE FUNCTION get_user_doc(p_id INTEGER)
RETURNS VARCHAR
LANGUAGE plpgsql
AS $$
DECLARE
    doc VARCHAR;
BEGIN
    SELECT b.cpf INTO doc
    FROM brazilians b
    WHERE b.user_id = p_id
    LIMIT 1;

    IF doc IS NULL THEN
        SELECT f.rnm INTO doc
        FROM foreigners f
        WHERE f.user_id = p_id
        LIMIT 1;
    END IF;

    RETURN doc;
END;
$$;

CREATE FUNCTION get_user_by_id(p_id INTEGER)
RETURNS SETOF user_public
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT u.id,
           u.name,
           u.email,
           u.birthday,
           u.sex,
           u.icon,
           get_user_doc(u.id)
    FROM users u
    WHERE u.id = p_id
    LIMIT 1;
END;
$$;

CREATE FUNCTION get_user_by_email(p_email VARCHAR)
RETURNS SETOF user_public
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT u.id,
           u.name,
           u.email,
           u.birthday,
           u.sex,
           u.icon,
           get_user_doc(u.id)
    FROM users u
    WHERE u.email = p_email
    LIMIT 1;
END;
$$;

CREATE FUNCTION confirm_user(
    p_email VARCHAR,
    p_password VARCHAR
) RETURNS SETOF user_public
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT u.id,
           u.name,
           u.email,
           u.birthday,
           u.sex,
           u.icon,
           get_user_doc(u.id)
    FROM users u
    WHERE u.email = p_email
    AND u.password = p_password
    LIMIT 1;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'User not found';
    END IF;
END;
$$;

-----------------------------------------------------------------
---------------------------Caronista-----------------------------
-----------------------------------------------------------------

CREATE TABLE drivers (
    cnh VARCHAR(11) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    rating FLOAT NOT NULL,
    preferences VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE FUNCTION create_driver(
    p_user_id INTEGER,
    p_cnh VARCHAR,
    p_preferences VARCHAR
) RETURNS SETOF drivers
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO drivers (cnh, user_id, rating, preferences)
    VALUES (p_cnh, p_user_id, 0, p_preferences);

    RETURN QUERY
    SELECT *
    FROM drivers
    WHERE user_id = p_user_id
    LIMIT 1;
END;
$$;

CREATE FUNCTION get_driver(p_user_id INTEGER)
RETURNS SETOF drivers
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM drivers
    WHERE user_id = p_user_id;
END;
$$;

CREATE TABLE cars (
    renavam VARCHAR(11) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    plate VARCHAR(7) NOT NULL,
    color VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE FUNCTION create_car(
    p_renavam VARCHAR(11),
    p_user_id INTEGER,
    p_brand VARCHAR(50),
    p_model VARCHAR(50),
    p_plate VARCHAR(7),
    p_color VARCHAR(50)
) RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO cars (renavam, user_id, brand, model, plate, color)
    VALUES (p_renavam, p_user_id, p_brand, p_model, p_plate, p_color);
END;
$$;

CREATE FUNCTION get_car_by_renavam(p_renavam VARCHAR)
RETURNS SETOF cars
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM cars
    WHERE renavam = p_renavam
    LIMIT 1;
END;
$$;

CREATE FUNCTION get_cars_by_user_id(p_user_id INTEGER)
RETURNS SETOF cars
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM cars
    WHERE user_id = p_user_id;
END;
$$;

-----------------------------------------------------------------
---------------------------VIAGEM--------------------------------
-----------------------------------------------------------------
CREATE TYPE direction AS ENUM ('PICK_UP', 'PICK_OFF', 'MIDDLE');

CREATE TABLE address (
    id SERIAL PRIMARY KEY,
    cep VARCHAR(9) NOT NULL,
    street VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL,
    district VARCHAR(50) NOT NULL,
    house_number VARCHAR(5) NOT NULL,
    direction direction NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE FUNCTION create_address(
    p_cep VARCHAR,
    p_street VARCHAR,
    p_city VARCHAR,
    p_state VARCHAR,
    p_district VARCHAR,
    p_house_number VARCHAR,
    p_direction direction,
    p_user_id INTEGER
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    address_id INTEGER;
BEGIN
    INSERT INTO address (cep, street, city, state, district, house_number, direction, user_id)
    VALUES (p_cep, p_street, p_city, p_state, p_district, p_house_number, p_direction, p_user_id)
    RETURNING id INTO address_id;

    RETURN address_id;
END;
$$;

CREATE FUNCTION get_address_by_id(
    p_id INTEGER
) RETURNS SETOF address
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM address
    WHERE id = p_id;
END;
$$;

CREATE TABLE origins (
    id SERIAL PRIMARY KEY,
    address_id INTEGER NOT NULL,
    space INTEGER NOT NULL,
    FOREIGN KEY (address_id) REFERENCES address(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE middles (
    id SERIAL PRIMARY KEY,
    address_id INTEGER NOT NULL,
    space INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    distance VARCHAR(100) NOT NULL,
    origin_id INTEGER NOT NULL,
    price FLOAT NOT NULL,
    FOREIGN KEY (origin_id) REFERENCES origins(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (address_id) REFERENCES address(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE destinations (
    id SERIAL PRIMARY KEY,
    address_id INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    distance VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    origin_id INTEGER,
    middle_id INTEGER,
    FOREIGN KEY (address_id) REFERENCES address(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (origin_id) REFERENCES origins(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (middle_id) REFERENCES middles(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE travels (
    id SERIAL PRIMARY KEY,
    status BOOLEAN NOT NULL,
    user_id INTEGER NOT NULL,
    renavam VARCHAR(11) NOT NULL,
    departure TIMESTAMP WITH TIME ZONE NOT NULL,
    origin_id INTEGER NOT NULL,
    middle_id INTEGER,
    destination_id INTEGER NOT NULL,
    arrival TIMESTAMP WITH TIME ZONE NOT NULL,
    involved INTEGER[] CHECK (array_length(involved, 1) <= 4),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (renavam) REFERENCES cars(renavam) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (origin_id) REFERENCES origins(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (middle_id) REFERENCES middles(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (destination_id) REFERENCES destinations(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE FUNCTION create_origin(
    p_address_id INTEGER,
    p_space INTEGER
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO origins(address_id, space)
    VALUES(p_address_id, p_space)
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$;

CREATE FUNCTION create_middle(
    p_address_id INTEGER,
    p_space INTEGER,
    p_duration INTEGER,
    p_distance VARCHAR(100),
    p_origin_id INTEGER
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
    p_price FLOAT;
BEGIN
    p_price := 35 + (p_duration / 3600.0) * 10;
    
    INSERT INTO middles(address_id, space, duration, distance, price, origin_id)
    VALUES(p_address_id, p_space, p_duration, p_distance, p_price, p_origin_id)
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$;

CREATE FUNCTION create_destination(
    p_address_id INTEGER,
    p_duration INTEGER,
    p_distance VARCHAR(100),
    p_origin_id INTEGER,
    p_middle_id INTEGER
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
    p_price FLOAT;
BEGIN
    p_price := 35 + (p_duration / 3600.0) * 10;
    
    INSERT INTO destinations(address_id, duration, distance, price, origin_id, middle_id)
    VALUES(p_address_id, p_duration, p_distance, p_price, p_origin_id, p_middle_id)
    RETURNING id INTO v_id;

    RETURN v_id;
END;
$$;

CREATE FUNCTION _create_travel(
    p_origin_address_id INTEGER,
    p_space INTEGER,
    p_middle_address_id INTEGER,
    p_middle_duration INTEGER,
    p_middle_distance VARCHAR(100),
    p_destination_address_id INTEGER,
    p_destination_duration INTEGER,
    p_destination_distance VARCHAR(100)
) RETURNS TABLE(origin_id INTEGER, middle_id INTEGER, destination_id INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
    v_origin_id INTEGER;
    v_middle_id INTEGER;
    v_destination_id INTEGER;
BEGIN
    v_origin_id := create_origin(p_origin_address_id, p_space);
    
    IF p_middle_address_id IS NOT NULL THEN
        v_middle_id := create_middle(p_middle_address_id, p_space, p_middle_duration, p_middle_distance, v_origin_id);
    ELSE
        v_middle_id := NULL;
    END IF;

    v_destination_id := create_destination(p_destination_address_id, p_destination_duration, p_destination_distance, v_origin_id, v_middle_id);

    RETURN QUERY SELECT v_origin_id, v_middle_id, v_destination_id;
END;
$$;


CREATE FUNCTION valid_travel(
    p_user_id INTEGER,
    p_departure TIMESTAMP WITH TIME ZONE,
    p_arrival TIMESTAMP WITH TIME ZONE 
) RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
    is_valid BOOLEAN := TRUE;
BEGIN
    IF EXISTS (
        SELECT 1
        FROM travels
        WHERE user_id = p_user_id AND status = TRUE
        AND (
            (p_departure < arrival AND p_arrival > departure)
        )
    ) THEN
        is_valid := FALSE;
    END IF;
    RETURN is_valid;
END;
$$;

CREATE FUNCTION create_travel(
    p_user_id INTEGER,
    p_renavam VARCHAR,
    p_space INTEGER,
    p_departure TIMESTAMP WITH TIME ZONE,
    p_origin_address_id INTEGER,
    p_middle_address_id INTEGER,
    p_middle_duration INTEGER,
    p_middle_distance VARCHAR,
    p_destination_address_id INTEGER,
    p_destination_duration INTEGER,
    p_destination_distance VARCHAR
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_origin_id INTEGER;
    v_middle_id INTEGER;
    v_destination_id INTEGER;
    v_id INTEGER;
    v_arrival TIMESTAMP WITH TIME ZONE;
BEGIN
    SELECT origin_id, middle_id, destination_id INTO
        v_origin_id, v_middle_id, v_destination_id
    FROM _create_travel(
        p_origin_address_id,
        p_space,
        p_middle_address_id,
        p_middle_duration,
        p_middle_distance,
        p_destination_address_id,
        p_destination_duration,
        p_destination_distance
    );
    v_arrival := p_departure + ((COALESCE(p_middle_duration, 0) + COALESCE(p_destination_duration, 0)) * INTERVAL '1 second');

    IF valid_travel(p_user_id, p_departure, v_arrival) THEN
        INSERT INTO travels(status, user_id, renavam, departure, origin_id, middle_id, destination_id, arrival, )
        VALUES (TRUE, p_user_id, p_renavam, p_departure, v_origin_id, v_middle_id, v_destination_id, v_arrival)
        RETURNING id INTO v_id;
        RETURN v_id;
    ELSE
        RAISE EXCEPTION 'INVALID TRAVEL';
    END IF;
END;
$$;


CREATE FUNCTION get_travel(
    p_id INTEGER
) RETURNS SETOF travels
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM travels WHERE id = p_id;
END;
$$;

CREATE FUNCTION get_travel_by_user_id(
    p_user_id INTEGER
) RETURNS TABLE (
    travel_id INTEGER,
    status TEXT,
    user_id INTEGER,
    renavam TEXT,
    departure TIMESTAMP WITH TIME ZONE,
    origin_address_id INTEGER,
    origin_space TEXT,
    origin_address TEXT,
    middle_address_id INTEGER,
    middle_space TEXT,
    middle_duration INTERVAL,
    middle_distance FLOAT,
    middle_price NUMERIC,
    middle_address TEXT,
    destination_address_id INTEGER,
    destination_duration INTERVAL,
    destination_distance FLOAT,
    destination_price NUMERIC,
    destination_address TEXT,
    arrival TIMESTAMP WITH TIME ZONE,
    involved TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        t.id AS travel_id,
        t.status,
        t.user_id,
        t.renavam,
        t.departure,
        o.address_id AS origin_address_id,
        o.space AS origin_space,
        a1.address AS origin_address,
        m.address_id AS middle_address_id,
        m.space AS middle_space,
        m.duration AS middle_duration,
        m.distance AS middle_distance,
        m.price AS middle_price,
        a2.address AS middle_address,
        d.address_id AS destination_address_id,
        d.duration AS destination_duration,
        d.distance AS destination_distance,
        d.price AS destination_price,
        a3.address AS destination_address,
        t.arrival,
        t.involved
    FROM 
        travels t
    LEFT JOIN origins o ON t.origin_id = o.id
    LEFT JOIN address a1 ON o.address_id = a1.id
    LEFT JOIN middles m ON t.middle_id = m.id
    LEFT JOIN address a2 ON m.address_id = a2.id
    LEFT JOIN destinations d ON t.destination_id = d.id
    LEFT JOIN address a3 ON d.address_id = a3.id
    WHERE t.user_id = p_user_id;
END;
$$;



-----------------------------------------------------------------
---------------------------AVALIACAO-------------------------------
-----------------------------------------------------------------

--criacao da tabela de avaliacao
CREATE TYPE tipo_avaliacao AS ENUM ('CARONISTA', 'CARONEIRO');
CREATE TYPE nota_avaliacao AS ENUM ('PESSIMO', 'RUIM', 'MEDIANO', 'BOM', 'OTIMO');
CREATE TABLE Avalia (
    id SERIAL PRIMARY KEY,
    id_autor INTEGER NOT NULL,
    id_destinatario INTEGER NOT NULL,
    criacao TIMESTAMP NOT NULL,
    tipo_de_avaliado tipo_avaliacao NOT NULL,
    nota nota_avaliacao NOT NULL,
    conteudo VARCHAR(255),
    FOREIGN KEY (id_autor) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_destinatario) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

--função para criar uma avaliacao nova
CREATE FUNCTION create_avaliacao(
    p_id_autor INTEGER,
    p_id_destinatario INTEGER,
    p_tipo_de_avaliado tipo_avaliacao,
    p_nota nota_avaliacao,
    p_conteudo VARCHAR(255)
) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_avaliacao INTEGER;
BEGIN
    -- Insere a nova avaliação na tabela Avalia
    INSERT INTO Avalia (id_autor, id_destinatario, criacao, tipo_de_avaliado, nota, conteudo)
    VALUES (p_id_autor, p_id_destinatario, NOW(), p_tipo_de_avaliado, p_nota, p_conteudo)
    RETURNING id INTO v_id_avaliacao;

    -- Retorna o ID da avaliação recém-criada
    RETURN v_id_avaliacao;
END;
$$;

--procedimento que mostra os detalhes dos usuarios que estavam em uma carona
CREATE OR REPLACE FUNCTION get_trip_participants(
    p_user_id INTEGER,  -- ID do usuário que está fazendo a consulta
    p_travel_id INTEGER -- ID da viagem que se deseja consultar
)
RETURNS TABLE (
    participant_id INTEGER,
    name VARCHAR,
    email VARCHAR,
    gender gender,
    birthday DATE
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Retornar detalhes de todos os participantes da viagem especificada
    RETURN QUERY
    SELECT u.id AS participant_id,
           u.name,
           u.email,
           u.sex AS gender,
           u.birthday
    FROM users u
    INNER JOIN travels t ON u.id = t.user_id
    WHERE t.id = p_travel_id
      AND u.id != p_user_id;
END;
$$;

--funcao que atualiza as avaliacoes medias de um usuario
CREATE OR REPLACE FUNCTION atualizar_avaliacao_media()
RETURNS TRIGGER AS $$
DECLARE
    nova_media FLOAT;
BEGIN
    -- Calcular a nova média das avaliações para o usuário avaliado
    SELECT AVG(CASE
                 WHEN nota = 'PESSIMO' THEN 1
                 WHEN nota = 'RUIM' THEN 2
                 WHEN nota = 'MEDIANO' THEN 3
                 WHEN nota = 'BOM' THEN 4
                 WHEN nota = 'OTIMO' THEN 5
               END) INTO nova_media
    FROM Avalia
    WHERE id_destinatario = NEW.id_destinatario;

    -- Atualizar a coluna de avaliação média do usuário
    UPDATE users
    SET avaliacao_media = nova_media
    WHERE id = NEW.id_destinatario;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


--trigger ativado apos uma avaliacao ser feita para atualizar a avaliacao media de um usuario
CREATE TRIGGER trigger_atualizar_avaliacao_media
AFTER INSERT ON Avalia
FOR EACH ROW
EXECUTE FUNCTION atualizar_avaliacao_media();

--view dos detalhes de uma avaliacao feita
CREATE VIEW view_detalhes_avaliacoes AS
SELECT
    a.id AS avaliacao_id,
    a.criacao AS data_avaliacao,
    u_autor.name AS nome_autor,
    u_autor.email AS email_autor,
    u_destinatario.name AS nome_destinatario,
    u_destinatario.email AS email_destinatario,
    a.tipo_de_avaliado AS tipo_avaliacao,
    a.nota AS nota_avaliacao,
    a.conteudo AS conteudo_avaliacao
FROM
    Avalia a
JOIN
    users u_autor ON a.id_autor = u_autor.id
JOIN
    users u_destinatario ON a.id_destinatario = u_destinatario.id;

