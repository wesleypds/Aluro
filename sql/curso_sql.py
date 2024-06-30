SQL_CRIAR_TABELA_CURSO = """
    CREATE TABLE IF NOT EXISTS curso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        url TEXT NOT NULL
    )
"""

SQL_INSERIR_CURSO = """
    INSERT INTO curso(nome, descricao, url)
    VALUES (?, ?, ?)
"""

SQL_OBTER_TODOS_CURSOS = """
    SELECT id, nome, descricao, url
    FROM curso
    ORDER BY nome
"""

SQL_ALTERAR_CURSO = """
    UPDATE curso
    SET nome=?, descricao=?, url=?
    WHERE id=?
"""

SQL_EXCLUIR_CURSO = """
    DELETE FROM curso    
    WHERE id=?
"""

SQL_OBTER_UM_CURSO = """
    SELECT id, nome, descricao, url
    FROM curso
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE_CURSO = """
    SELECT COUNT(*) 
    FROM curso
"""

SQL_OBTER_BUSCA_CURSO = """
    SELECT id, nome, descricao, url
    FROM curso
    WHERE nome LIKE ? OR descricao LIKE ?
    ORDER BY nome
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA_CURSO = """
    SELECT COUNT(*) 
    FROM curso
    WHERE nome LIKE ? OR descricao LIKE ?
"""