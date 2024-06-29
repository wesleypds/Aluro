SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS aluno_curso (
        id_curso INTEGER NOT NULL,
        id_categoria INTEGER NOT NULL,
        PRIMARY KEY(id_curso, id_aluno),
        FOREIGN KEY (id_curso) REFERENCES curso(id),
        FOREIGN KEY (id_aluno) REFERENCES aluno(id))
"""

SQL_INSERIR = """
    INSERT INTO aluno_curso(id_curso, id_aluno)
    VALUES (?, ?)
"""

SQL_OBTER_POR_PEDIDO = """
    SELECT id_curso, id_aluno
    FROM aluno_curso
    WHERE id_curso=?
"""

SQL_OBTER_QUANTIDADE_POR_PRODUTO = """
    SELECT quantidade
    FROM aluno_curso
    WHERE id_curso=? AND id_aluno=?
"""

SQL_ALTERAR_VALOR_PRODUTO = """
    UPDATE aluno_curso
    SET valor_produto=?
    WHERE id_curso=? AND id_aluno=?
"""

SQL_ALTERAR_QUANTIDADE_PRODUTO = """
    UPDATE aluno_curso
    SET quantidade=?
    WHERE id_curso=? AND id_aluno=?
"""

SQL_AUMENTAR_QUANTIDADE_PRODUTO = """
    UPDATE aluno_curso
    SET quantidade=quantidade+1
    WHERE id_curso=? AND id_aluno=?
"""

SQL_DIMINUIR_QUANTIDADE_PRODUTO = """
    UPDATE aluno_curso
    SET quantidade=quantidade-1
    WHERE id_curso=? AND id_aluno=?
"""

SQL_EXCLUIR = """
    DELETE FROM aluno_curso
    WHERE id_curso=? AND id_aluno=?
"""

SQL_OBTER_QUANTIDADE_POR_PEDIDO = """
    SELECT COUNT(*) FROM aluno_curso
    WHERE id_curso=?
"""
