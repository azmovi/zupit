def test_user_insertion(connection):
    _, cursor = connection
    cursor.execute("""
        INSERT INTO users (username, email, password) VALUES(
        'test_user',
        'test_user@dominio.com',
        'test_password');"""
    )
    cursor.execute(
        "SELECT * FROM users WHERE username = 'test_user'"
    )
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == 1
    assert result[1] == 'test_user'
    assert result[2] == 'test_user@dominio.com'
    assert result[3] == 'test_password'
