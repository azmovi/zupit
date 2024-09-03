from fastapi import Form
from pydantic import BaseModel, validator


class Car(BaseModel):
    renavam: str
    user_id: int
    brand: str
    model: str
    plate: str
    color: str

    @validator('renavam')
    def validate_renavam(cls, v):
        # Verifica se possui 11 dígitos
        if len(v) != 11 or not v.isdigit():
            raise ValueError('RENAVAM deve ter 11 dígitos numéricos')
        
        # Cálculo do dígito verificador do RENAVAM
        multiplicadores = [2, 3, 4, 5, 6, 7, 8, 9]
        renavam_reversed = list(map(int, v[::-1]))
        
        soma = sum(renavam_reversed[i] * multiplicadores[i % len(multiplicadores)] for i in range(1, 11))
        resto = soma % 11
        digito_verificador = 11 - resto if resto >= 2 else 0
        # Verifica se o digito verificador é igual ao esperado
        if digito_verificador != renavam_reversed[0]:
            raise ValueError('RENAVAM inválido')

        return v

    @classmethod
    def as_form(
        cls,
        renavam: str = Form(...),
        user_id: int = Form(...),
        brand: str = Form(...),
        model: str = Form(...),
        plate: str = Form(...),
        color: str = Form(...),
    ):
        return cls(
            renavam=renavam,
            user_id=user_id,
            brand=brand,
            model=model,
            plate=plate,
            color=color,
        )


class CarList(BaseModel):
    cars: list[Car]
