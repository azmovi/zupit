from sqlalchemy import text

query = text(
    """
             SELECT
    table_schema,
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM
    information_schema.columns
WHERE
    table_schema NOT IN ('information_schema', 'pg_catalog')
ORDER BY
    table_schema,
    table_name,
    ordinal_position;

"""
)


def test_func_db(session):
    try:
        result = session.execute(query)
        print(result)
        functions = result.fetchall()

        print('oi')
        for row in functions:
            print(row)

    except Exception as e:
        print(e)

    finally:
        print('aqui')
        session.close()
