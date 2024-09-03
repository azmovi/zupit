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
    cnh VARCHAR(9) PRIMARY KEY,
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
---------------------------VIAGEM-------------------------------
-----------------------------------------------------------------

CREATE TYPE direction AS ENUM ('PICK_UP', 'PICK_OFF');

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


CREATE TABLE travels (
    id SERIAL PRIMARY KEY,
    status BOOLEAN NOT NULL,
    user_id INTEGER NOT NULL,
    renavam VARCHAR(11) NOT NULL,
    space INTEGER NOT NULL,
    departure_date DATE NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    origin_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,
    distance VARCHAR(50) NOT NULL,
    duration VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (renavam) REFERENCES cars(renavam) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (origin_id) REFERENCES address(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (destination_id) REFERENCES address(id) ON DELETE CASCADE ON UPDATE CASCADE
);

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
    -- Retornar detalhes de todos os participantes da viagem
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
