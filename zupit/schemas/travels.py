from typing import Optional
from datetime import date, time


from pydantic import BaseModel

class Address(BaseModel):
    cep: str
    street: str
    district: str
    city: str
    state: str
    house_number: str

class Travel(BaseModel):
    status: bool
    user_id: int
    renavam: str
    space: int
    departure_date: date
    departure_time: time
    pick_up: Address
    pick_off: Address
    # duration: time
