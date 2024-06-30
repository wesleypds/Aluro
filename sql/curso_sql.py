SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS curso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        url TEXT NOT NULL)
"""

SQL_INSERIR = """
    INSERT INTO curso(nome, descricao, url)
    VALUES (?, ?, ?)
"""

SQL_OBTER_TODOS = """
    SELECT id, nome, descricao, url
    FROM curso
    ORDER BY nome
"""

SQL_ALTERAR = """
    UPDATE curso
    SET nome=?, descricao=?, url=?
    WHERE id=?
"""

SQL_EXCLUIR = """
    DELETE FROM curso    
    WHERE id=?
"""

SQL_OBTER_UM = """
    SELECT id, nome, descricao, url
    FROM curso
    WHERE id=?
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) 
    FROM curso
"""

SQL_OBTER_BUSCA = """
    SELECT id, nome, descricao, url
    FROM curso
    ORDER BY nome
    LIMIT ? OFFSET ?
"""

SQL_OBTER_QUANTIDADE_BUSCA = """
    SELECT COUNT(*) 
    FROM curso
    WHERE nome LIKE ? OR descricao LIKE ?
"""