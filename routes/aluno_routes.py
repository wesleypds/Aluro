from datetime import datetime
from fastapi import APIRouter, Form, Query, Request, status
from fastapi.responses import JSONResponse, RedirectResponse

from dtos.alterar_aluno_dto import AlterarAlunoDTO
from dtos.alterar_senha_dto import AlterarSenhaDTO
from models.aluno_curso_model import AlunoCurso
from models.aluno_model import Aluno
from repositories.aluno_curso_repo import AlunoCursoRepo
from repositories.aluno_repo import AlunoRepo
from repositories.curso_repo import CursoRepo
from util.auth import conferir_senha, obter_hash_senha
from util.cookies import (
    adicionar_mensagem_alerta,
    adicionar_mensagem_erro,
    adicionar_mensagem_sucesso,
    excluir_cookie_auth,
)
from util.templates import obter_jinja_templates

router = APIRouter(prefix="/aluno")
templates = obter_jinja_templates("templates/aluno")


@router.get("/cursos")
async def get_pedidos(request: Request):
    return templates.TemplateResponse(
        "pages/cursos.html",
        {"request": request},
    )


@router.get("/cadastro")
async def get_cadastro(request: Request):
    return templates.TemplateResponse(
        "pages/cadastro.html",
        {
            "request": request,
        },
    )


@router.post("/post_cadastro", response_class=JSONResponse)
async def post_cadastro(request: Request, alterar_dto: AlterarAlunoDTO):
    id = request.state.aluno.id
    aluno_data = alterar_dto.model_dump()
    response = JSONResponse({"redirect": {"url": "/aluno/cadastro"}})
    if AlunoRepo.alterar(Aluno(id, **aluno_data)):
        adicionar_mensagem_sucesso(response, "Cadastro alterado com sucesso!")
    else:
        adicionar_mensagem_erro(
            response, "Não foi possível alterar os dados cadastrais!"
        )
    return response


@router.get("/senha")
async def get_senha(request: Request):
    return templates.TemplateResponse(
        "pages/senha.html",
        {"request": request},
    )


@router.post("/post_senha", response_class=JSONResponse)
async def post_senha(request: Request, alterar_dto: AlterarSenhaDTO):
    email = request.state.aluno.email
    aluno_bd = AlunoRepo.obter_por_email(email)
    nova_senha_hash = obter_hash_senha(alterar_dto.nova_senha)
    response = JSONResponse({"redirect": {"url": "/aluno/senha"}})
    if not conferir_senha(alterar_dto.senha, aluno_bd.senha):
        adicionar_mensagem_erro(response, "Senha atual incorreta!")
        return response
    if AlunoRepo.alterar_senha(aluno_bd.id, nova_senha_hash):
        adicionar_mensagem_sucesso(response, "Senha alterada com sucesso!")
    else:
        adicionar_mensagem_erro(response, "Não foi possível alterar sua senha!")
    return response



@router.get("/sair", response_class=RedirectResponse)
async def get_sair(request: Request):
    if request.state.aluno:
        AlunoRepo.alterar_token(request.state.aluno.email, "")
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    excluir_cookie_auth(response)
    adicionar_mensagem_sucesso(response, "Saída realizada com sucesso!")
    return response


@router.get("/curso")
async def get_carrinho(request: Request):
    aluno_curso = AlunoCursoRepo.obter_por_aluno(request.state.aluno.id)
    cursos = []
    for ac in aluno_curso:
        curso = CursoRepo.obter_um(ac.id_curso)
        if curso:
            cursos.append(curso) 
    return templates.TemplateResponse(
        "pages/curso_inscrito.html",
        {"request": request, "itens": cursos},
    )

@router.post("/post_adicionar_curso", response_class=RedirectResponse)
async def post_adicionar_curso(request: Request, id_curso: int = Form(...)):
    curso = CursoRepo.obter_um(id_curso)
    id_aluno = request.state.aluno.id
    aluno_curso = AlunoCurso(None, curso.nome, curso.id, id_aluno)
    inscricao = AlunoCursoRepo.inserir(aluno_curso)
    mensagem = f"O curso <b>{curso.nome}</b> foi inscrito."
    response = RedirectResponse("/aluno/curso", status.HTTP_303_SEE_OTHER)
    adicionar_mensagem_sucesso(response, mensagem)
    return response

@router.post("/post_desiscrever", response_class=RedirectResponse)
async def post_desiscrever(request: Request, id_curso: int = Form(0)):
    curso = CursoRepo.obter_um(id_curso)
    desinscricao = AlunoCursoRepo.excluir(id_curso)
    mensagem = f"Você não é mais inscrito no curso <b>{curso.nome}</b>."
    response = RedirectResponse("/aluno/curso", status.HTTP_303_SEE_OTHER)
    adicionar_mensagem_sucesso(response, mensagem)
    return response

@router.post("/post_visualizar", response_class=RedirectResponse)
async def post_visualizar(request: Request, id_curso: int = Form(0)):
    curso = CursoRepo.obter_um(id_curso)
    return templates.TemplateResponse(
        "pages/visualizacao.html",
        {"request": request, "curso": curso},
    )