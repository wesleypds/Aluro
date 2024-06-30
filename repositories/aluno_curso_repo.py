import json
import pdb
import sqlite3
from typing import List, Optional
from models.aluno_curso_model import AlunoCurso
from sql.aluno_curso_sql import *
from util.database import obter_conexao


class AlunoCursoRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, aluno_curso: AlunoCurso) -> Optional[AlunoCurso]:
        try:
            with obter_conexao() as conexao:
                print(aluno_curso.id_aluno)
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        aluno_curso.nome_curso,
                        aluno_curso.id_curso,
                        aluno_curso.id_aluno,
                    ),
                )
                if cursor.rowcount > 0:
                    aluno_curso.id = cursor.lastrowid
                    return aluno_curso
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_por_aluno(cls, id: int) -> List[AlunoCurso]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_POR_ALUNO, (id,)).fetchall()
                aluno_cursos = [AlunoCurso(*t) for t in tuplas]
                return aluno_cursos
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def excluir(cls, id: int) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_EXCLUIR, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

