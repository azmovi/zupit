from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from zupit.schemas.avalia import Avalia


def create_avaliacao_db(avaliacao: Avalia, session: Session):
    sql = text(
        """
        SELECT * FROM create_avaliacao(
            :id_autor, :id_destinatario, :tipo_de_avaliado, :nota, :conteudo
        )"""
    )

    try:
        session.execute(
            sql,
            {
                'id_autor': avaliacao.id_autor,
                'id_destinatario': avaliacao.id_destinatario,
                'tipo_de_avaliado': avaliacao.tipo_de_avaliado.value,
                'nota': avaliacao.nota.value,
                'conteudo': avaliacao.conteudo,
            },
        )
        session.commit()

    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Input invalid'
        )


def get_avaliacao_db(avaliacao_id: int, session: Session):
    sql = text(
        """
        SELECT * FROM view_detalhes_avaliacoes
        WHERE avaliacao_id = :avaliacao_id
        """
    )

    try:
        result = session.execute(
            sql,
            {
                'avaliacao_id': avaliacao_id,
            },
        ).fetchone()

        if result is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='Avaliacao nao encontrada',
            )

        avaliacao = {
            'avaliacao_id': result.avaliacao_id,
            'data_avaliacao': result.data_avaliacao,
            'nome_autor': result.nome_autor,
            'email_autor': result.email_autor,
            'nome_destinatario': result.nome_destinatario,
            'email_destinatario': result.email_destinatario,
            'tipo_avaliacao': result.tipo_avaliacao,
            'nota_avaliacao': result.nota_avaliacao,
            'conteudo_avaliacao': result.conteudo_avaliacao,
        }

        return avaliacao

    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Erro ao buscar avaliacao',
        )
