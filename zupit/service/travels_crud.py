from typing import Annotated, Optional

from fastapi import Depends
from googlemaps import Client
from sqlalchemy.orm import Session

from zupit.database import get_session
from zupit.schemas.travels import Travel
from zupit.settings import Settings

Session = Annotated[Session, Depends(get_session)]

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


def valid_travel(
    session: Session, # type: ignore
    travel: Travel
) -> bool:
    return True


def create_travel_db(
    session: Session, # type: ignore 
    travel: Travel
) -> bool:
    # TODO Fazer isso primeiro
    return True
