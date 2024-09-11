from datetime import date, time
from typing import Optional

from pydantic import BaseModel, Field, model_validator

from zupit.utils import get_distance


class Address(BaseModel):
    id: Optional[int] = None
    cep: str
    street: str
    district: str
    city: str
    state: str
    house_number: str
    direction: str
    user_id: int


class Travel(BaseModel):
    status: bool = Field(default_factory=lambda: True)
    user_id: int
    renavam: str
    space: int
    departure_date: date
    departure_time: time
    pick_up: Address
    pick_off: Address
    distance: Optional[str] = None
    duration: Optional[str] = None
    price: Optional[float] = None

    @model_validator(mode='after')
    def calculate_metrics(self):
        from zupit.service.travels_crud import get_distance
        origin = self.pick_up.cep
        destination = self.pick_off.cep

        result = get_distance(origin, destination)

        if result:
            self.distance, self.duration = result
        return self

    @model_validator(mode='after')
    def calculate_price(self):
        if self.distance:
            distance = int(self.distance.split()[0])
            self.price = 30 + 0.25 * distance
        return self
