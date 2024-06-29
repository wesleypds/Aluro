import json
import sqlite3
from typing import List, Optional
from models.aluno_model import Aluno
from sql.aluno_sql import *
from util.database import obter_conexao


class AlunoRepo:

    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA)

    @classmethod
    def inserir(cls, aluno: Aluno) -> Optional[Aluno]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR,
                    (
                        aluno.nome,
                        aluno.cpf,
                        aluno.data_nascimento,
                        aluno.endereco,
                        aluno.telefone,
                        aluno.email,
                        aluno.senha,
                    ),
                )
                if cursor.rowcount > 0:
                    aluno.id = cursor.lastrowid
                    return aluno
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_todos(cls) -> List[Aluno]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS).fetchall()
                alunos = [Aluno(*t) for t in tuplas]
                return alunos
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar(cls, aluno: Aluno) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR,
                    (
                        aluno.nome,
                        aluno.cpf,
                        aluno.data_nascimento,
                        aluno.endereco,
                        aluno.telefone,
                        aluno.email,
                        aluno.id,
                    ),
                )
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

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

    @classmethod
    def obter_por_id(cls, id: int) -> Optional[Aluno]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_ID, (id,)).fetchone()
                aluno = Aluno(*tupla)
                return aluno
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_quantidade(cls) -> Optional[int]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def inserir_alunos_json(cls, arquivo_json: str):
        if AlunoRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                alunos = json.load(arquivo)
                for aluno in alunos:
                    AlunoRepo.inserir(Aluno(**aluno))

    @classmethod
    def obter_busca(cls, termo: str, pagina: int, tamanho_pagina: int) -> List[Aluno]:
        termo = "%" + termo + "%"
        offset = (pagina - 1) * tamanho_pagina
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(
                    SQL_OBTER_BUSCA, (termo, termo, tamanho_pagina, offset)
                ).fetchall()
                alunos = [Aluno(*t) for t in tuplas]
                return alunos
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_quantidade_busca(cls, termo: str) -> Optional[int]:
        termo = "%" + termo + "%"
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(
                    SQL_OBTER_QUANTIDADE_BUSCA, (termo, termo)
                ).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_por_email(cls, email: str) -> Optional[Aluno]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_EMAIL, (email,)).fetchone()
                if tupla:
                    aluno = Aluno(*tupla)
                    return aluno
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar_token(cls, id: int, token: str) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR_TOKEN, (token, id))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def obter_por_token(cls, token: str) -> Optional[Aluno]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_POR_TOKEN, (token,)).fetchone()
                if tupla:
                    aluno = Aluno(*tupla)
                    return aluno
                else:
                    return None
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar_senha(cls, id: int, senha: str) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ALTERAR_SENHA, (senha, id))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False
