from http import HTTPStatus
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.travels import Address, Travel, TravelPublic

Session = Annotated[Session, Depends(get_session)]


# def valid_travel(
#     session: Session,  # type: ignore
#     travel: Travel,
# ) -> bool:
#     sql = text('SELECT * FROM valid_travel(:user_id, :departure, :arrival)')
#     try:
#         result = session.execute(
#             sql,
#             {
#                 'user_id': travel.user_id,
#                 'departure': travel.departure,
#                 'arrival': travel.arrival,
#             },
#         )
#         session.commit()
#         return result.fetchone()[0]
#     except Exception:
#         session.rollback()
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
#         )


def create_travel_db(
    session: Session,  # type: ignore
    travel: Travel,
) -> int:
    middle_address_id = None
    origin_address_id = create_address_db(session, travel.origin)
    if travel.middle:
        middle_address_id = create_address_db(session, travel.middle)
    destination_address_id = create_address_db(session, travel.destination)

    sql = text(
        """
    SELECT * FROM create_travel(
        :user_id,
        :renavam,
        :space,
        :origin_address_id,
        :origin_departure,
        :middle_address_id,
        :middle_duration,
        :middle_distance,
        :destination_address_id,
        :destination_duration,
        :destination_distance
    )
    """
    )
    try:
        result = session.execute(
            sql,
            {
                'user_id': travel.user_id,
                'renavam': travel.renavam,
                'space': travel.space,
                'origin_address_id': origin_address_id,
                'origin_departure': travel.departure,
                'middle_address_id': middle_address_id,
                'middle_duration': travel.middle_duration,
                'middle_distance': travel.middle_distance,
                'destination_address_id': destination_address_id,
                'destination_duration': travel.destination_duration,
                'destination_distance': travel.destination_distance,
            },
        )
        id = result.fetchone()[0]
        session.commit()
        return id
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=f'Input invalid {e}'
        )


def get_travel_db(
    session: Session,
    id: int,  # type: ignore
) -> Optional[TravelPublic]:
    sql = text('SELECT * FROM get_travel(:id)')
    result = session.execute(sql, {'id': id}).fetchone()
    session.commit()
    if result:
        return TravelPublic(
            id=result[0],
            status=result[1],
            user_id=result[2],
            renavam=result[3],
            origin_id=result[4],
            middle_id=result[5],
            destination_id=result[6],
        )
    return None


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
            session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.NOT_ACCEPTABLE,
                detail='Address not create',
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )


def get_address_db(
    session: Session,  # type: ignore
    address_id: int,
) -> Address:
    sql = text('SELECT * FROM get_address_by_id(:id)')
    try:
        result = session.execute(sql, {'id': address_id})
        address_db = result.fetchone()
        session.commit()
        if address_db:
            return Address(
                id=address_db[0],
                cep=address_db[1],
                street=address_db[2],
                city=address_db[3],
                state=address_db[4],
                district=address_db[5],
                house_number=address_db[6],
                direction=address_db[7],
                user_id=address_db[8],
            )
        else:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Address not found',
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )
