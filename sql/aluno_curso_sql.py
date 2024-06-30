SQL_CRIAR_TABELA = """
    CREATE TABLE IF NOT EXISTS aluno_curso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_curso TEXT NOT NULL,
        id_curso INTEGER NOT NULL,
        id_aluno INTEGER NOT NULL,
        FOREIGN KEY (id_curso) REFERENCES curso(id),
        FOREIGN KEY (id_aluno) REFERENCES aluno(id)
    )
"""

SQL_INSERIR = """
    INSERT INTO aluno_curso(nome_curso, id_curso, id_aluno)
    VALUES (?, ?, ?)
"""

SQL_OBTER_POR_ALUNO = """
    SELECT *
    FROM aluno_curso
    WHERE id_aluno=?
"""

SQL_EXCLUIR = """
    DELETE FROM aluno_curso
    WHERE id_curso=?
"""
