from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.cars import Car, CarList
from zupit.service.cars_crud import create_car_db, get_car_db, get_cars_db

router = APIRouter(prefix='/cars', tags=['cars'])


@router.post(
    '/',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def create_car(
    request: Request,
    session: Session = Depends(get_session),
    car: Car = Depends(Car.as_form),
):
    try:
        result = get_car_db(car.renavam, session)
        if result:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Car already exists'
            )

        create_car_db(car, session)
        return RedirectResponse(url='/offer', status_code=HTTPStatus.SEE_OTHER)

    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(url='/car', status_code=HTTPStatus.SEE_OTHER)


@router.get('/{user_id}/', response_model=CarList)
def get_cars(
    user_id: int, session: Session = Depends(get_session)
) -> Optional[CarList]:
    if car_list := get_cars_db(user_id, session):
        return car_list
    return None
