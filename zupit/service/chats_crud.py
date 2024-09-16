from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.chats import Chat, ChatList

Session = Annotated[Session, Depends(get_session)]


def create_chat_db(
    session: Session,  # type: ignore
    first: int,
    second: int,
):
    sql = text('SELECT * FROM create_chat(:first, :second)')
    try:
        session.execute(sql, {'first': first, 'second': second})
        session.commit()
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Invalid chat creation'
        )


def get_chats_db(
    session: Session,  # type: ignore
    user_id: int,
) -> Optional[ChatList]:
    chat_list = []
    sql = text('SELECT * FROM get_chats(:user_id)')
    chats = session.execute(sql, {'user_id': user_id}).fetchall()
    for chat in chats:
        chat_example = Chat(
            id=chat[0],
            first=chat[1],
            second=chat[2],
        )
        chat_list.append(chat_example)

    return ChatList(chats=chat_list)
