from typing import Optional

from pydantic import BaseModel
from fastapi import Form

class Driver(BaseModel):
    user_id: int
    cnh: str
    rating: float
    preferences: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        user_id: int = Form(...),
        cnh: str = Form(...),
        preferences: str = Form(None),
    ):
        return cls(
            user_id=user_id,
            cnh=cnh,
            preferences=preferences,
            rating=0.0,
        )


class DriverPublic(BaseModel):
    id: int
    cnh: str
    rating: float
    preferences: Optional[str] = None
