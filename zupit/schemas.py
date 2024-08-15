from datetime import date
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel


class Gender(Enum):
    MAN = 'MAN'
    WOMAN = 'WOMAN'


class Nacionality(Enum):
    BRAZILIAN = 'BRAZILIAN'
    FOREIGNER = 'FOREIGNER'


class User(BaseModel):
    name: str
    email: str
    password: str
    birthday: date
    sex: Gender
    nationality: Nacionality
    cpf: Optional[str] = None
    rnm: Optional[str] = None


class Brazilian(BaseModel):
    id: int
    name: str
    email: str
    birthday: date
    sex: Gender
    cpf: str


class Foreigner(BaseModel):
    id: int
    name: str
    email: str
    birthday: date
    sex: Gender
    rnm: str


UserPublic = Union[Brazilian, Foreigner]
