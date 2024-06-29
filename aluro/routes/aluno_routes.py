from datetime import datetime
from fastapi import APIRouter, Form, Query, Request, status
from fastapi.responses import JSONResponse, RedirectResponse

from dtos.alterar_aluno_dto import AlterarAlunoDTO
from dtos.alterar_senha_dto import AlterarSenhaDTO
from models.aluno_model import Aluno
# from models.item_pedido_model import ItemPedido
# from models.pedido_model import Pedido
from repositories.aluno_repo import AlunoRepo
# from repositories.item_pedido_repo import ItemPedidoRepo
# from repositories.pedido_repo import PedidoRepo
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


# @router.get("/carrinho")
# async def get_carrinho(request: Request, id_curso: int = Query(0)):
    
    
#     pedidos = PedidoRepo.obter_por_estado(request.state.aluno.id, 1)
#     pedido_carrinho = pedidos[0] if pedidos else None
#     if pedido_carrinho:
#         itens_pedido = ItemPedidoRepo.obter_por_pedido(pedido_carrinho.id)
#     return templates.TemplateResponse(
#         "pages/carrinho.html",
#         {"request": request, "itens": itens_pedido},
#     )

# @router.post("/post_adicionar_carrinho", response_class=RedirectResponse)
# async def post_adicionar_carrinho(request: Request, id_curso: int = Form(...)):
#     curso = CursoRepo.obter_um(id_curso)
#     mensagem = f"O curso <b>{curso.nome}</b> foi adicionado ao carrinho."    
#     pedidos = PedidoRepo.obter_por_estado(request.state.aluno.id, 1)
#     pedido_carrinho = pedidos[0] if pedidos else None        
#     if pedido_carrinho == None:
#         pedido_carrinho = Pedido(0, datetime.now(), 0, request.state.aluno.endereco, 1, request.state.aluno.id)
#         pedido_carrinho = PedidoRepo.inserir(pedido_carrinho)
#     qtde = ItemPedidoRepo.obter_quantidade_por_curso(pedido_carrinho.id, id_curso)
#     if qtde == 0:            
#         item_pedido = ItemPedido(pedido_carrinho.id, id_curso, curso.nome, curso.preco, 1, 0)
#         ItemPedidoRepo.inserir(item_pedido)            
#     else:
#         ItemPedidoRepo.aumentar_quantidade_curso(pedido_carrinho.id, id_curso)
#         mensagem = f"O curso <b>{curso.nome}</b> já estava no carrinho e teve sua quantidade aumentada."        
#     response = RedirectResponse("/aluno/carrinho", status.HTTP_303_SEE_OTHER)
#     adicionar_mensagem_sucesso(response, mensagem)
#     return response

# @router.post("/post_aumentar_item", response_class=RedirectResponse)
# async def post_aumentar_item(request: Request, id_curso: int = Form(0)):
#     curso = CursoRepo.obter_um(id_curso)
#     pedidos = PedidoRepo.obter_por_estado(request.state.aluno.id, 1)
#     pedido_carrinho = pedidos[0] if pedidos else None
    
#     if pedido_carrinho == None:
#         response = RedirectResponse(f"/curso?id={id_curso}", status.HTTP_303_SEE_OTHER)
#         adicionar_mensagem_alerta(f"Seu carrinho não foi encontrado. Adicione este curso ao carrinho novamente.")
#         return response

#     qtde = ItemPedidoRepo.obter_quantidade_por_curso(pedido_carrinho.id, id_curso)
#     if qtde == 0:
#         response = RedirectResponse(f"/curso?id={id_curso}", status.HTTP_303_SEE_OTHER)
#         adicionar_mensagem_alerta(f"Este curso não foi encontrado em seu carrinho. Adicione-o novamente.")
#         return response
    
#     ItemPedidoRepo.aumentar_quantidade_curso(pedido_carrinho.id, id_curso)
#     response = RedirectResponse("/aluno/carrinho", status.HTTP_303_SEE_OTHER)
#     adicionar_mensagem_sucesso(response, f"O curso <b>{curso.nome}</b> teve sua quantidade aumentada para <b>{qtde+1}</b>.")
#     return response

# @router.post("/post_reduzir_item", response_class=RedirectResponse)
# async def post_reduzir_item(request: Request, id_curso: int = Form(0)):
#     curso = CursoRepo.obter_um(id_curso)
#     pedidos = PedidoRepo.obter_por_estado(request.state.aluno.id, 1)
#     pedido_carrinho = pedidos[0] if pedidos else None
#     response = RedirectResponse("/aluno/carrinho", status.HTTP_303_SEE_OTHER)
    
#     if pedido_carrinho == None:        
#         adicionar_mensagem_alerta(f"Seu carrinho não foi encontrado.")
#         return response

#     qtde = ItemPedidoRepo.obter_quantidade_por_curso(pedido_carrinho.id, id_curso)
#     if qtde == 0:        
#         adicionar_mensagem_alerta(f"O curso {id_curso} não foi encontrado em seu carrinho.")
#         return response
    
#     if qtde == 1:
#         ItemPedidoRepo.excluir(pedido_carrinho.id, id_curso)        
#         adicionar_mensagem_sucesso(response, f"O curso <b>{curso.nome}</b> foi excluído do carrinho.")
#         return response
    
#     ItemPedidoRepo.diminuir_quantidade_curso(pedido_carrinho.id, id_curso)    
#     adicionar_mensagem_sucesso(response, f"O curso <b>{curso.nome}</b> teve sua quantidade diminuída para <b>{qtde+1}</b>.")
#     return response