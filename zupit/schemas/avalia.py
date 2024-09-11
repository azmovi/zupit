from enum import Enum
from typing import Optional

from fastapi import Form
from pydantic import BaseModel


class tipo_avaliacao(Enum):
    CARONISTA = 'CARONISTA'
    CARONEIRO = 'CARONEIRO'


class nota_avaliacao(Enum):
    PESSIMO = 'PESSIMO'
    RUIM = 'RUIM'
    MEDIANO = 'MEDIANO'
    BOM = 'BOM'
    OTIMO = 'OTIMO'


class Avalia(BaseModel):
    id_autor: int
    id_destinatario: int
    tipo_de_avaliado: tipo_avaliacao
    nota: nota_avaliacao
    conteudo: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        id_autor: int = Form(...),
        id_destinatario: int = Form(...),
        tipo_de_avaliado: str = Form(...),
        nota: str = Form(...),
        conteudo: Optional[str] = Form(None),
    ):
        return cls(
            id_autor=id_autor,
            id_destinatario=id_destinatario,
            tipo_de_avaliado=tipo_avaliacao(tipo_de_avaliado),
            nota=nota_avaliacao(nota),
            conteudo=conteudo,
        )
