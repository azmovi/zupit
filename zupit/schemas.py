from datetime import date
from enum import Enum
from typing import Optional, Union

from fastapi import Form
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

    @classmethod
    def as_form(
        cls,
        name: str = Form(),
        email: str = Form(),
        password: str = Form(),
        birthday: str = Form(),
        sex: str = Form(),
        nationality: str = Form(),
        cpf: Optional[str] = Form(None),
        rnm: Optional[str] = Form(None),
    ):
        return cls(
            name=name,
            email=email,
            password=password,
            birthday=date.fromisoformat(birthday),
            sex=Gender(sex),
            nationality=Nationality(nationality),
            cpf=cpf,
            rnm=rnm,
        )


class Public(BaseModel):
    id: int
    name: str
    email: EmailStr
    birthday: date
    sex: Gender
    icon: Optional[bytes]
    doc: str


class Brazilian(BaseModel):
    id: int
    name: str
    email: EmailStr
    birthday: date
    sex: Gender
    icon: Optional[bytes] = None
    cpf: str


class Foreigner(BaseModel):
    id: int
    name: str
    email: EmailStr
    birthday: date
    sex: Gender
    icon: Optional[bytes] = None
    rnm: str


UserPublic = Union[Brazilian, Foreigner, Public]


class UserCredentials(BaseModel):
    email: str
    password: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(),
        password: str = Form(),
    ):
        return cls(
            email=email,
            password=password,
        )


class Driver(BaseModel):
    user_id: int
    cnh: str
    rating: float
    preferences: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        user_id: int = Form(),
        cnh: str = Form(),
        preferences: str = Form(),
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
