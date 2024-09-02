from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.travels import Travel
from zupit.service.travels_crud import valid_travel, create_travel_db

router = APIRouter(prefix='/travels', tags=['travels'])

Session = Annotated[Session, Depends(get_session)]


@router.post('/', response_model=bool)
def crate_travel(
    request: Request,
    session: Session,  # type: ignore
    travel: Travel,
):
    if valid_travel(session, session):
        create_travel_db(session, travel)
    return True
