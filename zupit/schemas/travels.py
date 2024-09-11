from datetime import datetime
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


class Origin(BaseModel):
    address: Address
    departure: datetime
    space: int


class Middle(BaseModel):
    address: Address
    duration: int
    distance: str
    space: int
    price: float
    origin_id: int


class Destination(BaseModel):
    address: Address
    arrival: datetime
    distance: str
    price: float
    origin_id: Optional[int] = Field(default_factory=None)
    middle_id: Optional[int] = Field(default_factory=None)


class Travel(BaseModel):
    user_id: int
    renavam: str
    space: int
    departure: datetime
    origin: Address
    middle: Optional[Address] = Field(default=None)
    destination: Address
    middle_distance: Optional[str] = Field(default=None)
    middle_duration: Optional[int] = Field(default=None)
    destination_distance: Optional[str] = Field(default=None)
    destination_duration: Optional[int] = Field(default=None)

    @model_validator(mode='after')
    def calculate_metrics(self):
        origin = self.origin.cep
        middle = None
        if self.middle:
            middle = self.middle.cep
        destination = self.destination.cep

        result = get_distance(origin, destination, middle)
        if result:
            if middle_results := result.get('middle', None):
                self.middle_distance, self.middle_duration = middle_results
            if destination_results := result.get('destination', None):
                (
                    self.destination_distance,
                    self.destination_duration,
                ) = destination_results
        else:
            raise ValueError('Invalid cep')
        return self


class TravelPublic(BaseModel):
    id: int
    status: bool
    user_id: int
    renavam: str
    origin_id: int
    middle_id: Optional[int]
    destination_id: int
