SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
"""

SQL_INSERIR = """
    INSERT INTO categoria(nome)
    VALUES (?)
"""
