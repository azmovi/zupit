from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.travels import Address, Travel

Session = Annotated[Session, Depends(get_session)]


def valid_travel(
    session: Session,  # type: ignore
    travel: Travel,
) -> bool:
    return True


def create_travel_db(
    session: Session,  # type: ignore
    travel: Travel,
) -> bool:
    origin_id = create_address_db(session, travel.pick_up)
    destination_id = create_address_db(session, travel.pick_off)

    sql = text("""
    SELECT * FROM create_travel(
        :user_id,
        :renavam,
        :space,
        :departure_date,
        :departure_time,
        :origin_id,
        :destination_id,
        :distance,
        :duration
    )
   """)
    try:
        result = session.execute(
            sql,
            {
                'user_id': travel.user_id,
                'renavam': travel.renavam,
                'space': travel.space,
                'departure_date': travel.departure_date,
                'departure_time': travel.departure_time,
                'origin_id': origin_id,
                'destination_id': destination_id,
                'distance': travel.distance,
                'duration': travel.duration,
            },
        )
        session.commit()
        return result
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )


def create_address_db(
    session: Session,  # type: ignore
    address: Address,
) -> int:
    sql = text(
        """SELECT * FROM create_address(
            :cep,
            :street,
            :city,
            :state,
            :district,
            :house_number,
            :direction,
            :user_id
        )"""
    )
    address_dict = address.model_dump()
    try:
        result = session.execute(sql, address_dict)
        address_id = result.fetchone()[0]
        session.commit()
        if address_id:
            return address_id
        else:
            raise HTTPException(
                status_code=HTTPStatus.NOT_ACCEPTABLE,
                detail='Address not create',
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )
