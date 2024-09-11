from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.avalia import Avalia
from zupit.service.avalia_crud import create_avaliacao_db, get_avaliacao_db

router = APIRouter(prefix='/avalia', tags=['avalia'])


@router.post(
    '/',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def create_avaliacao(
    request: Request,
    session: Session = Depends(get_session),
    avalia: Avalia = Depends(Avalia.as_form),
) -> RedirectResponse:
    try:
        avaliacao_db = get_avaliacao_db(avalia.user_id, session)
        if avaliacao_db:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Avalia already exists'
            )
        create_avaliacao_db(avalia, session)
        request.session['avalia'] = True
        return RedirectResponse(url='/offer', status_code=HTTPStatus.SEE_OTHER)

    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/create-avalia', status_code=HTTPStatus.SEE_OTHER
        )


@router.get('/{user_id}', response_model=Avalia)
def get_avaliacao(user_id: int, session: Session = Depends(get_session)):
    db_user = get_avaliacao_db(user_id, session)
    if db_user:
        return db_user
    return None
