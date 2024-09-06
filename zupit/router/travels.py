from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.travels import Travel, TravelList
from zupit.service.travels_crud import create_travel_db, valid_travel, get_travels_db

router = APIRouter(prefix='/travels', tags=['travels'])


# Função POST para criar uma viagem
@router.post('/', response_model=bool)
def create_travel(
    travel: Travel,  # Objeto 'Travel' será passado no corpo da requisição
    session: Session = Depends(get_session),  # Injeção de dependência da sessão do banco de dados
):
    # Valida a viagem antes de criar
    if valid_travel(session, travel):
        create_travel_db(session, travel)
        return True
    raise HTTPException(status_code=400, detail="Invalid travel data")


# Função GET para obter viagens por user_id
@router.get('/{user_id}/', response_model=TravelList)
def get_travels(
    user_id: int,
    session: Session = Depends(get_session),
) -> TravelList:
    travel_list = get_travels_db(user_id, session)
    if travel_list:
        print(travel_list)  # Verifique se as viagens estão sendo recuperadas
        return travel_list
    raise HTTPException(status_code=404, detail="No travels found")

