from datetime import date, time
from typing import Optional

from pydantic import BaseModel, model_validator

from zupit.utils import get_distance


class Address(BaseModel):
    cep: str
    street: str
    district: str
    city: str
    state: str
    house_number: str
    direction: str
    user_id: int


class Travel(BaseModel):
    status: bool = True
    user_id: int
    renavam: str
    space: int
    departure_date: date
    departure_time: time
    pick_up: Address
    pick_off: Address
    distance: Optional[str] = None
    duration: Optional[str] = None

    @model_validator(mode='after')
    def calculate_metrics(self):
        origin = self.pick_up.cep
        destination = self.pick_off.cep

        result = get_distance(origin, destination)

        if result:
            self.distance, self.duration = result
        return self
