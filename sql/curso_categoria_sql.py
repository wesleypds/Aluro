SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS curso_categoria (
        id_curso INTEGER NOT NULL,
        id_categoria INTEGER NOT NULL,
        PRIMARY KEY(id_curso, id_categoria),
        FOREIGN KEY (id_curso) REFERENCES curso(id),
        FOREIGN KEY (id_categoria) REFERENCES categotia(id))
"""

SQL_INSERIR = """
    INSERT INTO curso_categoria(id_curso, id_categoria)
    VALUES (?, ?)
"""
