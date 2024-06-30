SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_curso INTEGER NOT NULL,
        FOREIGN KEY (id_curso) REFERENCES curso(id)
    );
"""

SQL_INSERIR = """
    INSERT INTO categoria(nome, id_curso)
    VALUES (?, ?)
"""

SQL_OBTER_QUANTIDADE = """
    SELECT COUNT(*) 
    FROM categoria
"""
SQL_OBTER_POR_CATEGORIA = """
    SELECT *
    FROM categoria
    WHERE nome LIKE ?
    LIMIT ? OFFSET ?
"""