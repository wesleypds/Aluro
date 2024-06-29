import secrets
from typing import Optional
import bcrypt
from fastapi import HTTPException, Request, status
from models.aluno_model import Aluno
from repositories.aluno_repo import AlunoRepo
from util.cookies import NOME_COOKIE_AUTH, adicionar_cookie_auth


async def obter_aluno_logado(request: Request) -> Optional[Aluno]:
    try:
        token = request.cookies[NOME_COOKIE_AUTH]
        if token.strip() == "":
            return None
        aluno = AlunoRepo.obter_por_token(token)
        return aluno
    except KeyError:
        return None


async def middleware_autenticacao(request: Request, call_next):
    aluno = await obter_aluno_logado(request)
    request.state.aluno = aluno
    response = await call_next(request)
    if response.status_code == status.HTTP_303_SEE_OTHER:
        return response
    if aluno:
        token = request.cookies[NOME_COOKIE_AUTH]
        adicionar_cookie_auth(response, token)
    return response


async def checar_permissao(request: Request):
    aluno = request.state.aluno if hasattr(request.state, "aluno") else None
    area_do_aluno = request.url.path.startswith("/aluno")
    area_do_admin = request.url.path.startswith("/admin")
    if (area_do_aluno or area_do_admin) and not aluno:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # if area_do_aluno and aluno.perfil != 1:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    # if area_do_admin and aluno.perfil != 2:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def obter_hash_senha(senha: str) -> str:
    try:
        hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        return hashed.decode()
    except ValueError:
        return ""


def conferir_senha(senha: str, hash_senha: str) -> bool:
    try:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    except ValueError:
        return False


def gerar_token(length: int = 32) -> str:
    try:
        return secrets.token_hex(length)
    except ValueError:
        return ""
