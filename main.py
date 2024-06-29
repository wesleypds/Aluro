from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from repositories.aluno_repo import AlunoRepo
# from repositories.item_pedido_repo import ItemPedidoRepo
# from repositories.pedido_repo import PedidoRepo
from repositories.curso_repo import CursoRepo
from routes import aluno_routes, main_routes
from util.auth import checar_permissao, middleware_autenticacao
from util.exceptions import configurar_excecoes

CursoRepo.criar_tabela()
CursoRepo.inserir_cursos_json("sql/curso.json")
AlunoRepo.criar_tabela()
AlunoRepo.inserir_alunos_json("sql/aluno.json")
# PedidoRepo.criar_tabela()
# ItemPedidoRepo.criar_tabela()
app = FastAPI(dependencies=[Depends(checar_permissao)])
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.middleware(middleware_type="http")(middleware_autenticacao)
configurar_excecoes(app)
app.include_router(main_routes.router)
app.include_router(aluno_routes.router)
