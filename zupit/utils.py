from typing import Optional

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.router.drivers import get_driver
from zupit.router.users import get_user
from zupit.schemas.driver import Driver
from zupit.schemas.user import UserPublic


def get_current_user(
    request: Request, session: Session = Depends(get_session)
) -> Optional[UserPublic]:
    if id := request.session.get('id'):
        return get_user(id, session)
    return None


def get_current_driver(
    request: Request, session: Session = Depends(get_session)
) -> Optional[Driver]:
    if id := request.session.get('id'):
        return get_driver(id, session)
    return None
