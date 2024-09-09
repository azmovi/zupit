from datetime import datetime, timedelta
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
    middle_space: int
    departure: datetime
    pick_up: Address
    middle: Optional[Address] = Field(default=None)
    pick_off: Address
    middle_distace: Optional[str] = Field(default=None)
    middle_duration: Optional[int] = Field(default=None)
    destination_distance: Optional[str] = Field(default=None)
    destination_duration: Optional[int] = Field(default=None)
    middle_arrival: Optional[datetime] = Field(default=None)
    destination_arrival: Optional[datetime] = Field(default=None)
    price: Optional[float] = Field(default=None)

    @model_validator(mode='after')
    def calculate_metrics(self):
        origin = self.pick_up.cep
        middle = None
        if self.middle:
            middle = self.middle.cep
        destination = self.pick_off.cep

        result = get_distance(origin, destination, middle)
        if result:
            if middle_results := result.get('middle', None):
                self.middle_distace, self.middle_duration = middle_results
            if destination_results := result.get('destination', None):
                (
                    self.destination_distance,
                    self.destination_duration,
                ) = destination_results
        else:
            raise ValueError('Invalid cep')
        return self

    @model_validator(mode='after')
    def arrival_previst(self):
        if self.destination_duration is not None:
            self.arrival = self.departure + timedelta(
                seconds=self.destination_duration
            )
        return self
