\c zupit_db

CREATE TYPE gender AS ENUM ('MAN', 'WOMAN');

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

CREATE FUNCTION get_user_by_email(p_email VARCHAR)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_user_id INTEGER;
BEGIN
    SELECT u.id INTO v_user_id
    FROM users u
    WHERE u.email = p_email
    LIMIT 1;

    RETURN v_user_id;
END;
$$;

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
)
RETURNS VOID
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
)
RETURNS TABLE (
    user_id INTEGER,
    user_name VARCHAR,
    user_email VARCHAR,
    user_birthday DATE,
    user_sex gender,
    brazilian_cpf VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE 
    v_user_id INTEGER;
BEGIN
    v_user_id := create_user(p_name, p_email, p_password, p_birthday, p_sex);
    PERFORM _create_brazilian(p_cpf, v_user_id);

    RETURN QUERY
    SELECT u.id, u.name, u.email, u.birthday, u.sex, b.cpf
    FROM users u
    JOIN brazilians b ON u.id = b.user_id
    WHERE u.id = v_user_id
    LIMIT 1;
END;
$$;

CREATE FUNCTION _create_foreigner(
    p_rnm VARCHAR,
    p_id_user INTEGER
)
RETURNS VOID
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
)
RETURNS TABLE (
    user_id INTEGER,
    user_name VARCHAR,
    user_email VARCHAR,
    user_birthday DATE,
    user_sex gender,
    foreigner_rnm VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE 
    v_user_id INTEGER;
BEGIN
    v_user_id := create_user(p_name, p_email, p_password, p_birthday, p_sex);
    PERFORM _create_foreigner(p_rnm, v_user_id);

    RETURN QUERY
    SELECT u.id, u.name, u.email, u.birthday, u.sex, f.rnm
    FROM users u
    JOIN foreigners f ON u.id = f.user_id
    WHERE u.id = v_user_id
    LIMIT 1;
END;
$$;

