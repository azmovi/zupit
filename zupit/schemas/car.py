from pydantic import BaseModel
from fastapi import Form

class Car(BaseModel):
    renavam: str
    brand: str
    model: str
    plate: str
    color: str

    @classmethod
    def as_form(
        cls,
        renavam: str = Form(...),
        brand: str = Form(...),
        model: str = Form(...),
        plate: str = Form(...),
        color: str = Form(...),
    ):
        return cls(
            renavam=renavam,
            brand=brand,
            model=model,
            plate=plate,
            color=color
        )
class CarList(BaseModel):
    cars: list[Car]
