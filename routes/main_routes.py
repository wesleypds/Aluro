import math
from sqlite3 import DatabaseError
from fastapi import APIRouter, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse

from dtos.entrar_dto import EntrarDTO
from util.html import ler_html
from dtos.novo_aluno_dto import NovoAlunoDTO
from models.aluno_model import Aluno
from repositories.aluno_repo import AlunoRepo
from repositories.curso_repo import CursoRepo
from util.auth import (
    conferir_senha,
    gerar_token,
    obter_hash_senha,
)

from util.cookies import adicionar_cookie_auth, adicionar_mensagem_sucesso
from util.pydantic import create_validation_errors
from util.templates import obter_jinja_templates

router = APIRouter()
templates = obter_jinja_templates("templates/main")


@router.get("/html/{arquivo}")
async def get_html(arquivo: str):
    response = HTMLResponse(ler_html(arquivo))
    return response


@router.get("/")
async def get_root(request: Request):
    cursos = CursoRepo.obter_todos()
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "cursos": cursos,
        },
    )


@router.get("/contato")
async def get_contato(request: Request):
    return templates.TemplateResponse(
        "pages/contato.html",
        {"request": request},
    )


@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse(
        "pages/cadastro.html",
        {"request": request},
    )
    
@router.get("/sobre")
async def get_grupo(request: Request):
    return templates.TemplateResponse(
        "pages/sobre.html",
        {"request": request},
    )


@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(aluno_dto: NovoAlunoDTO):
    aluno_data = aluno_dto.model_dump(exclude={"confirmacao_senha"})
    aluno_data["senha"] = obter_hash_senha(aluno_data["senha"])
    novo_aluno = AlunoRepo.inserir(Aluno(**aluno_data))
    if not novo_aluno or not novo_aluno.id:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar aluno.")
    return {"redirect": {"url": "/cadastro_realizado"}}


@router.get("/cadastro_realizado")
async def get_cadastro_realizado(request: Request):
    return templates.TemplateResponse(
        "pages/cadastro_confirmado.html",
        {"request": request},
    )


@router.get("/entrar")
async def get_entrar(
    request: Request,
    return_url: str = Query("/"),
):
    return templates.TemplateResponse(
        "pages/entrar.html",
        {
            "request": request,
            "return_url": return_url,
        },
    )


@router.post("/post_entrar", response_class=JSONResponse)
async def post_entrar(entrar_dto: EntrarDTO):
    aluno_entrou = AlunoRepo.obter_por_email(entrar_dto.email)
    if (
        (not aluno_entrou)
        or (not aluno_entrou.senha)
        or (not conferir_senha(entrar_dto.senha, aluno_entrou.senha))
    ):
        return JSONResponse(
            content=create_validation_errors(
                entrar_dto,
                ["email", "senha"],
                ["Credenciais inválidas.", "Credenciais inválidas."],
            ),
            status_code=status.HTTP_404_NOT_FOUND,
        )
    token = gerar_token()
    if not AlunoRepo.alterar_token(aluno_entrou.id, token):
        raise DatabaseError(
            "Não foi possível alterar o token do aluno no banco de dados."
        )
    response = JSONResponse(content={"redirect": {"url": entrar_dto.return_url}})
    adicionar_mensagem_sucesso(
        response,
        f"Olá, <b>{aluno_entrou.nome}</b>. Seja bem-vindo(a) ao Aluro, a sua plataforma de melhores cursos!",
    )
    adicionar_cookie_auth(response, token)
    return response


@router.get("/curso/{id:int}")
async def get_curso(request: Request, id: int):
    curso = CursoRepo.obter_um(id)
    return templates.TemplateResponse(
        "pages/curso.html",
        {
            "request": request,
            "curso": curso,
        },
    )


@router.get("/buscar")
async def get_buscar(
    request: Request,
    q: str,
    p: int = 1,
    tp: int = 6,
    o: int = 1,
):
    cursos = CursoRepo.obter_busca(q, p, tp, o)
    qtde_cursos = CursoRepo.obter_quantidade_busca(q)
    qtde_paginas = math.ceil(qtde_cursos / float(tp))
    return templates.TemplateResponse(
        "pages/buscar.html",
        {
            "request": request,
            "cursos": cursos,
            "quantidade_paginas": qtde_paginas,
            "tamanho_pagina": tp,
            "pagina_atual": p,
            "termo_busca": q,
            "ordem": o,
        },
    )
