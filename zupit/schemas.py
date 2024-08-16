from datetime import date
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, EmailStr


class Gender(Enum):
    MAN = 'MAN'
    WOMAN = 'WOMAN'


class Nationality(Enum):
    BRAZILIAN = 'BRAZILIAN'
    FOREIGNER = 'FOREIGNER'


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    birthday: date
    sex: Gender
    nationality: Nationality
    cpf: Optional[str] = None
    rnm: Optional[str] = None


class Public(BaseModel):
    id: int
    name: str
    email: EmailStr
    birthday: date
    sex: Gender


class Brazilian(BaseModel):
    id: int
    name: str
    email: EmailStr
    birthday: date
    sex: Gender
    cpf: str


class Foreigner(BaseModel):
    id: int
    name: str
    email: EmailStr
    birthday: date
    sex: Gender
    rnm: str


UserPublic = Union[Brazilian, Foreigner, Public]
