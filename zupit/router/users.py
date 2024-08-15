from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from zupit.database import Connection
from zupit.schemas import Brazilian, User, UserPublic

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=UserPublic,
    status_code=HTTPStatus.CREATED,
)
def create_user(user: User, conn: Connection):
    if user.nationality.value == 'BRAZILIAN':
        sql = """
            CALL create_brazilian(%s, %s, %s, %s, %s, %s);
        """
        try:
            with conn.cursor() as cur:
                cur.execute(
                    sql,
                    (
                        user.name,
                        user.email,
                        user.password,
                        user.birthday,
                        user.sex.value,
                        user.cpf,
                    ),
                )
                conn.commit()  # Commit da transação

            # Busca o usuário diretamente da tabela 'users'
            with conn.cursor() as cur:
                sql = """
                    SELECT u.id, u.name, u.email, u.birthday, u.sex, b.cpf
                    FROM users u JOIN brazilians b ON u.id = b.user_id
                    WHERE u.email = %s;
                """
                cur.execute(sql, (user.email,))
                user_db = cur.fetchone()

            if user_db is None:
                raise HTTPException(
                    status_code=404, detail='User not created.'
                )

            return Brazilian(
                id=user_db[0],
                name=user_db[1],
                email=user_db[2],
                birthday=user_db[3],
                sex=user_db[4],
                cpf=user_db[5],
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(
            status_code=402,
            detail=f'Unsupported nationality: {user.nationality}',
        )
