from http import HTTPStatus
from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.travels import Address, Travel, TravelList


# Função para validar uma viagem
def valid_travel(
    session: Session, 
    travel: Travel,
) -> bool:
    # Lógica de validação customizada aqui
    return True


# Função para criar uma viagem
def create_travel_db(
    travel: Travel,
    session: Session = Depends(get_session),  # Injeção de dependência da sessão
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
        return result.rowcount > 0  # Retorna True se a operação foi bem-sucedida
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )


# Função para criar um endereço
def create_address_db(
    address: Address,
    session: Session = Depends(get_session),  # Injeção de dependência da sessão
) -> int:
    sql = text("""
        SELECT * FROM create_address(
            :cep,
            :street,
            :city,
            :state,
            :district,
            :house_number,
            :direction,
            :user_id
        )
    """)
    address_dict = address.dict()  # Converte o objeto Address para um dicionário
    try:
        result = session.execute(sql, address_dict)
        address_id = result.fetchone()[0]
        session.commit()
        if address_id:
            return address_id
        else:
            raise HTTPException(
                status_code=HTTPStatus.NOT_ACCEPTABLE,
                detail='Address not created',
            )
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )


# Função para obter viagens por usuário
def get_travels_db(user_id: int, session: Session) -> TravelList:
    try:
        travel_list = []
        sql = text('SELECT * FROM get_travels_by_user_id(:user_id)')
        travels = session.execute(sql, {'user_id': user_id}).fetchall()
        print(f"Travels fetched for user_id {user_id}: {travels}")  # Log dos dados
        for travel in travels:
            travel_example = Travel(
                id=travel[0],
                status=travel[1],
                user_id=travel[2],
                renavam=travel[3],
                space=travel[4],
                departure_date=travel[5],
                departure_time=travel[6].time(),  # Extrai apenas o tempo do objeto datetime
                pick_up=get_address_db(travel[7], session),  # Converte o ID para Address
                pick_off=get_address_db(travel[8], session),  # Converte o ID para Address
                distance=travel[9],
                duration=travel[10],
            )
            travel_list.append(travel_example)

        return TravelList(travels=travel_list)
    except Exception as e:
        print(f"Error fetching travels: {str(e)}")  # Log do erro
        raise HTTPException(status_code=500, detail=str(e))



# Função para obter um endereço por ID
def get_address_db(
    address_id: int,
    session: Session = Depends(get_session),  # Injeção de dependência da sessão
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
