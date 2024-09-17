from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.service.chats_crud import (
    create_chat_db,
    get_chat_db,
    get_chats_db,
    get_messages_db,
)
from zupit.utils import get_current_user

router = APIRouter(prefix='/chats', tags=['chats'])
templates = Jinja2Templates(directory='zupit/templates')
Session = Annotated[Session, Depends(get_session)]


@router.post(
    '/{first}/{second}',
    response_class=HTMLResponse,
    status_code=HTTPStatus.CREATED,
)
def create_chat(
    request: Request,
    session: Session,  # type: ignore
    first: int,
    second: int,
):
    try:
        if not get_chat_db(session, first, second):
            create_chat_db(session, first, second)

        return RedirectResponse(url='/chats', status_code=HTTPStatus.SEE_OTHER)

    except HTTPException as exc:
        request.session['error'] = exc.detail
        return RedirectResponse(
            url='/search-travel', status_code=HTTPStatus.SEE_OTHER
        )


@router.get('/{user_id}/', response_class=HTMLResponse)
def get_chats(
    session: Session,  # type: ignore
    user_id: int,
):
    if chat_list := get_chats_db(session, user_id):
        return chat_list
    return None


@router.get('/{chat_id}/', response_class=HTMLResponse)
def get_messages(
    request: Request,
    session: Session,  # type: ignore
    chat_id: int,
):
    if user := get_current_user(request, session):
        messages = get_messages_db(session, chat_id)
        return templates.TemplateResponse(
            request=request,
            name='messages.html',
            context={'user': user, 'messages': messages.messages},
        )
    return RedirectResponse(url='sign-in', status_code=HTTPStatus.SEE_OTHER)


@router.get('/{first}/{second}', response_class=HTMLResponse)
def get_chat_by_users(
    request: Request,
    session: Session,  # type: ignore
    first: int,
    second: int,
):
    if first == second:
        return RedirectResponse(
            url=f'/trip-participants/{first}', status_code=HTTPStatus.SEE_OTHER
        )
    if chat_id := get_chat_db(session, first, second):
        return get_messages(request, session, chat_id)

    else:
        return create_chat(request, session, first, second)
