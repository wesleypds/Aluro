# A Fazer em 11 de Junho de 2024

## Cadastro do Aluno

- Acertar menu ativo do cabeçalho
- Adicionar SQL para tornar e revogar um aluno administrador
- Alterar SQL de Aluno e AlunoRepo.inserir para o campo telefone ficar logo após endereco
- Criar classe Aluno
- Criar repositório para a entidade aluno
- Criar página para cadastro de aluno
- Importar arquivo Python de validação de formulários (/util/validators.py)
- Criar DTO baseada em Pydantic para novo aluno
- Adicionar arquivos javascript para máscara e envio de formulário via JSON
- Adicionar atributo data-mask="..." aos inputs do cadastro de aluno
- Criar rota para cadastro de aluno (post) em main_routes.py
- Criar rota e página para cadastro confirmado (get) em main_routes.py
- Renomear arquivo para cadastro_confirmado.html

## Autenticação

- Alterar responsividade, botão "Entrar", links, action, json-form, button[submit] (entrar.html)
- Importar arquivo Python de autenticação (/util/auth.py)
- Importar arquivo Python de criação de cookies (/util/cookies.py)
- Importar arquivo Python para criação de validações customizadas com Pydantic (/util/pydantic.py)
- Importar arquivo Python para tratamento de exceções (/util/exceptions.py) e adicionar as páginas erro.html e 404.html
- Criar /dto/login_dto.py
- Adicionar método no repo para buscar aluno por email
- Adicionar método no repo para alterar token do aluno
- Adicionar método no repo para buscar aluno por token
- Adicionar aluno_logado: Aluno = Depends(obter_aluno_logado) como parâmetro de todas as rotas get e adicionar "aluno": aluno_logado ao modelo do template retornado
- Complementar o template header.html para mostrar estado do aluno (logado/deslogado)
- Criar rota para login (post) em main\_routes.py
- Adicionar middleware de atualização do token de autenticação
- Criar rota para logout (get) em main\_routes.py
- Elemento main do HTML foi movido para a página base e removido dos demais
- Criado o bloco topo na página base
- Carousel foi movido para um include
- Includes de exibição de mensagens por cookies adicionados à página base

## Carrinho e Pedidos

- Adicionar página do carrinho protegida somente para alunos
- Adicionar página de pedidos protegida somente para alunos

## Área Restrita

- Adicionar página do perfil protegida somente para alunos
