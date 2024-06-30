import json
import pdb
import sqlite3
from typing import List, Optional
from models.curso_model import Curso
from sql.curso_sql import *
from repositories.categoria_repo import *
from util.database import obter_conexao
import shutil
from pathlib import Path


class CursoRepo:
    
    @classmethod
    def criar_tabela(cls):
        with obter_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA_CURSO)

    @classmethod
    def inserir(cls, curso: Curso) -> Optional[Curso]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_INSERIR_CURSO,
                    (curso.nome, curso.descricao, curso.url),
                )
                if cursor.rowcount > 0:
                    curso.id = cursor.lastrowid
                    return curso
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_todos(cls) -> List[Curso]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tuplas = cursor.execute(SQL_OBTER_TODOS_CURSOS).fetchall()
                cursos = [Curso(*t) for t in tuplas]
                return cursos
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def alterar(cls, curso: Curso) -> bool:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    SQL_ALTERAR_CURSO,
                    (
                        curso.nome,
                        curso.descricao,
                        curso.url,
                        curso.id,
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
                cursor.execute(SQL_EXCLUIR_CURSO, (id,))
                return cursor.rowcount > 0
        except sqlite3.Error as ex:
            print(ex)
            return False

    @classmethod
    def obter_um(cls, id: int) -> Optional[Curso]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_UM_CURSO, (id,)).fetchone()
                curso = Curso(*tupla)
                return curso
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_quantidade(cls) -> Optional[int]:
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                tupla = cursor.execute(SQL_OBTER_QUANTIDADE_CURSO).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def obter_busca(
        cls, termo: str, pagina: int, tamanho_pagina: int, ordem: int
    ) -> List[Curso]:
        termo = "%" + termo + "%"
        offset = (pagina - 1) * tamanho_pagina
        try:
            with obter_conexao() as conexao:
                cursor = conexao.cursor()
                if ordem == 1:  
                    tuplas = cursor.execute(
                        SQL_OBTER_BUSCA_CURSO, (termo, termo, tamanho_pagina, offset)
                    ).fetchall()
                    cursos = [Curso(*t) for t in tuplas]
                    return cursos
                else:
                    match (ordem):
                        case 2:
                            termo = "%"+ "Front-End" +"%"
                        case 3:
                            termo = "%"+ "Back-End" +"%"
                        case 4:
                            termo = "%"+ "Eletrônica" +"%"
                    tuplas = cursor.execute(
                        SQL_OBTER_POR_CATEGORIA, (termo, tamanho_pagina, offset)
                    ).fetchall()
                    categorias = [Categoria(*t) for t in tuplas]
                    cursos = []
                    for categoria in categorias:
                        curso = CursoRepo.obter_um(categoria.id_curso)
                        if curso:
                            cursos.append(curso) 
                    return cursos
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
                    SQL_OBTER_QUANTIDADE_BUSCA_CURSO, (termo, termo)
                ).fetchone()
                return int(tupla[0])
        except sqlite3.Error as ex:
            print(ex)
            return None

    @classmethod
    def inserir_cursos_json(cls, arquivo_json: str):
        if CursoRepo.obter_quantidade() == 0:
            with open(arquivo_json, "r", encoding="utf-8") as arquivo:
                cursos = json.load(arquivo)
                for curso in cursos:
                    CursoRepo.inserir(Curso(**curso))
    #         cls.transferir_imagens("/static/img/cursos/inserir", "/static/img/cursos")

    # @classmethod
    # def transferir_imagens(cls, pasta_origem, pasta_destino):
    #     path_origem = Path(pasta_origem)
    #     path_destino = Path(pasta_destino)
    #     if not path_origem.exists() or not path_origem.is_dir():
    #         print(f"Pasta de origem {pasta_origem} não existe ou não é um diretório.")
    #         return
    #     if not path_destino.exists() or not path_destino.is_dir():
    #         print(f"Pasta de destino {pasta_destino} não existe ou não é um diretório.")
    #         return
    #     for arquivo_imagem in path_origem.glob("*"):
    #         if arquivo_imagem.is_file():
    #             path_arquivo_destino = path_destino / arquivo_imagem.name
    #             shutil.copy2(arquivo_imagem, path_arquivo_destino)
