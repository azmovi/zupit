from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from zupit.database import Connection
from zupit.schemas import Driver
from zupit.service.driver_crud import create_driver_db

router = APIRouter(prefix='/driver', tags=['driver'])


@router.post(
    '/',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def create_driver(
    request: Request,
    conn: Connection,
    driver: Driver = Depends(Driver.as_form),
) -> RedirectResponse:
    try:
        driver_db = create_driver_db(driver, conn)
        request.session['driver'] = driver_db

    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(url='/sign-up', status_code=exc.status_code)

    return driver_db


# @router.get(
#     '/{user_id}',
#     response_model=UserPublic,
# )
# def get_driver(user_id: int, conn: Connection):
#     db_user = get_driver_db(user_id, conn)
#     if db_user is None:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail='Driver not found'
#         )
#
#     return db_user
