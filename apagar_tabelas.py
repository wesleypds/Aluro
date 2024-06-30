import sqlite3

def apagar_todas_as_tabelas_menos_sqlite_sequence(db_name):
    # Conecta ao banco de dados
    conexao = sqlite3.connect(db_name)
    cursor = conexao.cursor()
    
    try:
        # Obtém a lista de todas as tabelas no banco de dados, exceto sqlite_sequence
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
        tabelas = cursor.fetchall()
        
        # Apaga cada tabela
        for tabela in tabelas:
            tabela_nome = tabela[0]
            print(f"Apagando a tabela: {tabela_nome}")
            cursor.execute(f"DROP TABLE IF EXISTS {tabela_nome};")
        
        # Confirma as mudanças
        conexao.commit()
        print("Todas as tabelas foram apagadas, exceto 'sqlite_sequence'.")
        
    except sqlite3.Error as e:
        print(f"Erro ao apagar as tabelas: {e}")
        
    finally:
        # Fecha a conexão com o banco de dados
        conexao.close()

# Use o nome do seu banco de dados SQLite aqui
db_name = 'dados.db'
apagar_todas_as_tabelas_menos_sqlite_sequence(db_name)
