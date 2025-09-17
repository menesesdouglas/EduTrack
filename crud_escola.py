import sqlite3
import time

# Nota para o futuro: Eu parei em def list_materiais()

def create_database():
    """Conecta ao banco de dados e cria as tabelas se elas não existirem"""
    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()

    # Cria a tabela Alunos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alunos(
            id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_aluno TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL,
            data_nascimento TEXT,
            telefone_responsavel TEXT,
            nome_responsavel TEXT,
            serie TEXT
        );
    """)

    # Cria a tabela Materias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Materias(
            id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_materia TEXT NOT NULL,
            codigo_materia TEXT UNIQUE NOT NULL
        );
    """)

    # Cria a tabela Notas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notas(
            id_nota INTEGER PRIMARY KEY AUTOINCREMENT,
            id_aluno INTEGER,
            id_materia INTEGER,
            trimestre INTEGER NOT NULL,
            nota REAL,
            FOREIGN KEY (id_aluno) REFERENCES Alunos(id_aluno) ON DELETE CASCADE,
            FOREIGN KEY (id_materia) REFERENCES Materias(id_materia) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()

def add_aluno(nome, matricula, data_nascimento, telefone, responsavel, serie):
    """Adiciona um novo aluno ao banco de dados"""
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Alunos (nome_aluno, matricula, data_nascimento, telefone_responsavel, nome_responsavel, serie) VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, matricula, data_nascimento, telefone, responsavel, serie))

        conn.commit()
        print(f"Aluno {nome} adicionado com sucesso.\n")
    except sqlite3.IntegrityError:
        print(f"Erro: A matrícula {matricula} já está no sistema.\n")
    except Exception as e:
        print(f"Ocorreu um erro. {e}\n")
    finally:
        conn.close()

def list_alunos():
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        cursor.execute("SELECT nome_aluno, matricula, serie FROM Alunos ORDER BY nome_aluno")
        alunos = cursor.fetchall()

        if not alunos:
            print("Nenhum aluno cadastrado.\n")
            return
        
        print("\n---Lista de Alunos---")
        for aluno in alunos:
            print(f"Nome: {aluno[0]} - Matrícula: {aluno[1]} - Série: {aluno[2]}")
        print("\n")
    except Exception as e:
        print(f"Ocorreu um erro. {e}\n")
    finally:
        conn.close()

def att_alunos(matricula_alvo, novo_nome, nova_serie):
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Alunos
            SET nome_aluno = ?, serie = ?
            WHERE matricula = ?
        """, (novo_nome, nova_serie, matricula_alvo))

        conn.commit()
        if cursor.rowcount > 0:
            print(f"Dados do aluno com matricula {matricula_alvo} foram atualizados.\n")
        else:
            print(f"Erro: Matrícula {matricula_alvo} não encontrada.\n")
        
    except Exception as e:
        print(f"Ocorreu um erro. {e}\n")
    finally:
        conn.close()

def remove_aluno(matricula_alvo):
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Alunos WHERE matricula = ?", (matricula_alvo,))

        conn.commit()
        if cursor.rowcount > 0:
            print(f"Aluno com matrícula {matricula_alvo} foi removido.\n")
        else:
            print(f"Erro: Matrícula {matricula_alvo} não encontrada.\n")
    
    except Exception as e:
        print(f"Ocorreu um erro. {e}\n")
    finally:
        conn.close()

def add_materia(nome, codigo):
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Materias (nome_materia, codigo_materia)
            VALUES (?, ?)
        """, (nome, codigo))
        
        conn.commit()
        print(f"Matéria {nome} cadastrada com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro. {e}")
    finally:
        conn.close()

def list_materias():
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        cursor.execute("SELECT nome_materia, codigo_materia FROM Materias ORDER BY nome_materia")
        materias = cursor.fetchall()

        if not materias:
            print("Nenhuma matéria cadastrada.")
            return

create_database()
print("Banco de dados 'escola.db' e tabelas criadas com sucesso.\n")
add_aluno("Teste", "203115", "17/09/2010", "(75)9 9999-9999", "Teste Pai", "3º Ano E.M.")
add_aluno("Teste 2", "4551121", "17/09/2011", "(75)9 9999-9323", "Teste Mãe", "1º Ano E.M.")
list_alunos()
att_alunos("203115", "Teste_Atualizado", "2º Ano E.M.")
list_alunos()
remove_aluno("4551121")
list_alunos()