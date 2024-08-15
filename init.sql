\c zupit_db

-- Criação do tipo ENUM 'gender'
CREATE TYPE gender AS ENUM ('MAN', 'WOMAN');

-- Criação da tabela 'users'
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(32) NOT NULL,
    birthday DATE NOT NULL,
    sex gender NOT NULL,
    icon BYTEA,
    user_status BOOLEAN NOT NULL
);

-- Criação da tabela 'brazilians'
CREATE TABLE IF NOT EXISTS brazilians (
    cpf VARCHAR(11) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Criação da tabela 'foreigners'
CREATE TABLE IF NOT EXISTS foreigners (
    rnm VARCHAR(8) PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Criação da função 'create_user'
CREATE OR REPLACE FUNCTION create_user(
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
    VALUES (
        p_name,
        p_email,
        p_password,
        p_birthday,
        p_sex,
        NULL,
        TRUE
    )
    RETURNING id INTO v_user_id;
    RETURN v_user_id;
END;
$$;

-- Criação do procedimento 'create_brazilian'
CREATE OR REPLACE PROCEDURE create_brazilian(
    p_name VARCHAR,
    p_email VARCHAR,
    p_password VARCHAR,
    p_birthday DATE,
    p_sex gender,
    p_cpf VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_user_id INTEGER;
BEGIN
    v_user_id := create_user(p_name, p_email, p_password, p_birthday, p_sex);
    
    INSERT INTO brazilians (cpf, user_id)
    VALUES (p_cpf, v_user_id);
END;
$$;

-- Criação do procedimento 'create_foreigner'
CREATE OR REPLACE PROCEDURE create_foreigner(
    p_name VARCHAR,
    p_email VARCHAR,
    p_password VARCHAR,
    p_birthday DATE,
    p_sex gender,
    p_rnm VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_user_id INTEGER;
BEGIN
    v_user_id := create_user(p_name, p_email, p_password, p_birthday, p_sex);
    
    INSERT INTO foreigners (rnm, user_id)
    VALUES (p_rnm, v_user_id);
END;
$$;

