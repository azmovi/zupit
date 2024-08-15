from enum import Enum
from typing import Optional

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
    birthday: str
    sex: Gender
    nationality: Nacionality
    cpf: Optional[str] = None
    rnm: Optional[str] = None


class Brazilian(BaseModel):
    name: str
    email: str
    birthday: str
    sex: Gender
    cpf: str


class Foreigner(BaseModel):
    name: str
    email: str
    birthday: str
    sex: Gender
    rnm: str
