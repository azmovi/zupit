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

CREATE TABLE drivers(
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
