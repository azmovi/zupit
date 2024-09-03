from typing import Annotated, Optional

from fastapi import Depends, Request
from googlemaps import Client
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.router.drivers import get_driver
from zupit.router.users import get_user
from zupit.schemas.drivers import Driver
from zupit.schemas.users import UserPublic
from zupit.settings import Settings

Session = Annotated[Session, Depends(get_session)]


def get_current_user(
    request: Request,
    session: Session,  # type: ignore
) -> Optional[UserPublic]:
    if id := request.session.get('id', None):
        return get_user(id, session)
    return None


def get_current_driver(
    request: Request,
    session: Session,  # type: ignore
) -> Optional[Driver]:
    if id := request.session.get('id'):
        if driver := get_driver(id, session):
            return driver
    return None


def get_distance(origin: str, destination: str) -> Optional[tuple[str, str]]:
    app = Client(Settings().API_KEY)  # type: ignore

    data = app.distance_matrix(
        origins=origin, destinations=destination, mode='driving'
    )
    rows = data.get('rows')[0]
    elements = rows.get('elements')[0]
    if elements.get('status') == 'OK':
        distance = elements.get('distance').get('text')
        duration = elements.get('duration').get('text')
        return distance, duration
    return None
