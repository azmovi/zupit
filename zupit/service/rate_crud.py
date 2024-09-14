from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.schemas.rate import Rate


def create_rating_db(rating: Rate, session: Session):
    sql = text(
        """
        SELECT * FROM create_rating(
            :author_id, :recipient_id, :rate_type, :grade, :content
        )"""
    )

    try:
        session.execute(
            sql,
            {
                'author_id': rating.author_id,
                'recipient_id': rating.recipient_id,
                'rate_type': rating.rate_type.value,
                'grade': rating.grade.value,
                'content': rating.content,
            },
        )
        session.commit()

    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )


def get_rating_db(recipient_id: int, session: Session) -> Optional[Rate]:
    sql = text(
        """
        SELECT id, author_id, recipient_id, rate_type, grade, content, creation
        FROM get_rating_by_recipient_id(:recipient_id);
        """
    )
    rate_db = session.execute(sql, {'recipient_id': recipient_id}).fetchone()
    session.commit()

    if rate_db:
        return Rate(
            id=rate_db[0],
            author_id=rate_db[1],
            recipient_id=rate_db[2],
            rate_type=rate_db[3],
            grade=rate_db[4],
            content=rate_db[5],
            creation=rate_db[6],
        )
    return None
