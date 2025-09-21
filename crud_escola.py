import sqlite3
import time

def create_database():
    """Conecta ao banco de dados e cria as tabelas se elas não existirem"""
    conn = sqlite3.connect('escola.db')  # Conecta ao banco (cria o arquivo se não existir)
    cursor = conn.cursor()

    # Cria a tabela Alunos para armazenar informações básicas dos estudantes
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

    # Cria a tabela Materias para armazenar as disciplinas oferecidas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Materias(
            id_materia INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_materia TEXT NOT NULL,
            codigo_materia TEXT UNIQUE NOT NULL
        );
    """)

    # Cria a tabela Notas para armazenar as notas de cada aluno por matéria e trimestre
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

    conn.commit()  # Salva as alterações no banco
    conn.close()   # Fecha a conexão

def add_aluno(nome, matricula, data_nascimento, telefone, responsavel, serie):
    """Adiciona um novo aluno ao banco de dados"""
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        # Insere um novo registro de aluno
        cursor.execute("""
            INSERT INTO Alunos (nome_aluno, matricula, data_nascimento, telefone_responsavel, nome_responsavel, serie) VALUES (?, ?, ?, ?, ?, ?)
        """, (nome, matricula, data_nascimento, telefone, responsavel, serie))

        conn.commit()
        print(f"Aluno {nome} adicionado com sucesso.\n")
    except sqlite3.IntegrityError:
        # Captura duplicidade de matrícula
        print(f"Erro: A matrícula {matricula} já está no sistema.\n")
    except Exception as e:
        print(f"Ocorreu um erro. {e}\n")
    finally:
        conn.close()

def list_alunos():
    """Lista todos os alunos cadastrados"""
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        cursor.execute("SELECT nome_aluno, matricula, serie FROM Alunos ORDER BY nome_aluno")
        alunos = cursor.fetchall()

        if not alunos:
            print("Nenhum aluno cadastrado.\n")
            return
        
        print("\n---Lista de Alunos---")
        # Exibe cada aluno com seus dados principais
        for aluno in alunos:
            print(f"Nome: {aluno[0]} - Matrícula: {aluno[1]} - Série: {aluno[2]}")
        print("\n")
    except Exception as e:
        print(f"Ocorreu um erro. {e}\n")
    finally:
        conn.close()

def att_alunos(matricula_alvo, novo_nome, nova_serie):
    """Atualiza o nome e/ou série de um aluno específico"""
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        # Atualiza os dados do aluno pela matrícula
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
    """Remove um aluno do banco de dados pela matrícula"""
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
    """Adiciona uma nova matéria ao banco de dados"""
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
    """Lista todas as matérias cadastradas"""
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        cursor.execute("SELECT nome_materia, codigo_materia FROM Materias ORDER BY nome_materia")
        materias = cursor.fetchall()

        if not materias:
            print("Nenhuma matéria cadastrada.")
            return
        print("\n--- Lista de Matérias---")
        # Exibe cada matéria com seu código
        for materia in materias:
            print(f"Nome: {materia[0]} - Código: {materia[1]}")
        print("\n")

    except Exception as e:
        print(f"Ocorreu um erro. {e}\n")
    finally:
        conn.close()

def att_materias(codigo_alvo, novo_nome):
    """Atualiza o nome de uma matéria existente"""
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Materias 
            SET nome_materia = ? 
            WHERE codigo_materia = ?
        """, (novo_nome, codigo_alvo))

        conn.commit()
        if cursor.rowcount > 0:
            print(f"Nome da matéria com código {codigo_alvo} atualizado para {novo_nome}.")
        else:
            print(f"Erro: Código da matéria {codigo_alvo} não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro. {e}")
    finally:
        conn.close()

def remove_materias(codigo_alvo):
    """Remove uma matéria do banco de dados pelo código"""
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Materias WHERE codigo_materia = ?", (codigo_alvo,))

        conn.commit()
        if cursor.rowcount > 0:
            print(f"Matéria com código {codigo_alvo} foi removido.\n")
        else:
            print(f"Erro: Código de matéria {codigo_alvo} não encontrada.\n")
    
    except Exception as e:
        print(f"Ocorreu um erro. {e}\n")
    finally:
        conn.close()

def get_aluno_id(matricula):
    """Obtém o ID interno do aluno pela matrícula"""
    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_aluno FROM Alunos WHERE matricula = ?", (matricula,))
    aluno_id = cursor.fetchone()
    conn.close()
    return aluno_id[0] if aluno_id else None

def get_materia_id(codigo_alvo):
    """Obtém o ID interno da matéria pelo código"""
    conn = sqlite3.connect('escola.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_materia FROM Materias WHERE codigo_materia = ?", (codigo_alvo,))
    materia_id = cursor.fetchone()
    conn.close()
    return materia_id[0] if materia_id else None

def adicionar_nota(matricula,materia,trimestre,nota):
    """Adiciona ou atualiza a nota de um aluno em uma matéria e trimestre"""
    aluno_id = get_aluno_id(matricula)
    materia_id = get_materia_id(materia)
    if not aluno_id:
        print(f"Erro: Aluno com matrícula {matricula} não encontrado.")
        return
    if not materia_id:
        print(f"Erro: Matéria com código {materia} não encontrado.")
        return
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        # Verifica se já existe uma nota para o aluno/matéria/trimestre
        cursor.execute("""
            SELECT id_nota FROM Notas
            WHERE id_aluno = ? AND id_materia = ? AND trimestre = ?
        """, (aluno_id,materia_id,trimestre))

        nota_existente = cursor.fetchone()

        if nota_existente:
            # Atualiza nota existente
            cursor.execute("""
                UPDATE Notas SET nota = ?
                WHERE id_nota = ?
            """, (nota, nota_existente[0]))
            print(f"Nota adicionada para o aluno {matricula} na materia {materia}.")
        else:
            # Insere uma nova nota se não existir
            cursor.execute("""
                INSERT INTO Notas (id_aluno, id_materia, trimestre, nota)
                VALUES (?, ?, ?, ?)
            """, (aluno_id, materia_id, trimestre, nota))
            print(f"Nota adicionada para o aluno {matricula} na matéria {materia} no {trimestre}º trimestre.")

        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro. {e}")
    finally:
        conn.close()

def gerar_relatorio_aluno(matricula, nota_minima_aprov=7.0, nota_maxima_reprov=4.9):
    """Gera um relatório de notas e situação final de um aluno"""
    aluno_id = get_aluno_id(matricula)
    if not aluno_id:
        print(f"Erro: O aluno {matricula} não foi encontrado.")
        return
    try:
        conn = sqlite3.connect('escola.db')
        cursor = conn.cursor()

        # Consulta todas as notas do aluno, organizadas por matéria e trimestre
        cursor.execute("""
            SELECT A.nome_aluno, M.nome_materia, N.trimestre, N.nota
            FROM Notas N
            JOIN Alunos A ON N.id_aluno = A.id_aluno
            JOIN Materias M ON N.id_materia = M.id_materia
            WHERE N.id_aluno = ?
            ORDER BY M.nome_materia, N.trimestre
        """, (aluno_id,))

        notas = cursor.fetchall()

        if not notas:
            print(f"Nenhuma nota encontrada para o aluno com matricula {matricula}.")
            return
        
        print(f"\n--- Relatório de Notas para o aluno {notas[0][0]} ({matricula}) ---")

        # Agrupa as notas por matéria para cálculo da média
        notas_por_materia = {}
        for nome_aluno, nome_materia, trimestre, nota in notas:
            if nome_materia not in notas_por_materia:
                notas_por_materia[nome_materia] = {}
            notas_por_materia[nome_materia][trimestre] = nota

        # Exibe as notas e calcula situação final por matéria
        for materia, notas_trimeste in notas_por_materia.items():
            print(f"\nMatéria: {materia}")
            soma_notas = 0
            count_trimestres = 0
            
            for trimestre in sorted(notas_trimeste.keys()):
                nota = notas_trimeste[trimestre]
                print(f" - Nota do {trimestre}º Trimestre: {nota}")
                soma_notas += nota
                count_trimestres += 1

            if count_trimestres == 3:
                nota_final = soma_notas / 3
                status = "Aprovado"
                if nota_final <= nota_maxima_reprov:
                    status = "Reprovado"
                elif nota_final < nota_minima_aprov:
                    status = "Recuperação"
                print(f" - Nota Final = {nota_final:.2f}")
                print(f" - Situação: {status}")
            else:
                print(" - Notas incompletas para cálculo da média final.")

    except Exception as e:
        print(f"Ocorreu um erro. {e}")
    finally:
        conn.close()

def menu_principal():
    """Menu principal para acessar os submenus do sistema"""
    while True:
        print("\n--- EduTrack - Sistema de Gestão Escolar ---")
        print("1. Gerenciar Alunos")
        print("2. Gerenciar Matérias")
        print("3. Gerenciar Notas")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")
        
        # Direciona para o menu escolhido
        if opcao == '1':
            menu_alunos()
        elif opcao == '2':
            menu_materias()
        elif opcao == '3':
            menu_notas()
        elif opcao == '4':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_alunos():
    """Menu para gerenciar alunos"""
    while True:
        print("\n--- Gerenciar Alunos ---")
        print("1. Adicionar Aluno")
        print("2. Listar Alunos")
        print("3. Atualizar Aluno")
        print("4. Remover Aluno")
        print("5. Voltar ao menu principal")
        
        opcao = input("Escolha uma opção: ")

        # Executa a ação de acordo com a escolha
        if opcao == '1':
            nome = input("Nome do aluno: ")
            matricula = input("Matrícula: ")
            data_nasc = input("Data de nascimento (dd/mm/aaaa): ")
            tel_resp = input("Telefone do responsável: ")
            nome_resp = input("Nome do responsável: ")
            serie = input("Série: ")
            add_aluno(nome, matricula, data_nasc, tel_resp, nome_resp, serie)
        elif opcao == '2':
            list_alunos()
        elif opcao == '3':
            matricula = input("Matrícula do aluno para atualizar: ")
            novo_nome = input("Novo nome (deixe em branco para não alterar): ")
            nova_serie = input("Nova série (deixe em branco para não alterar): ")
            # Atualiza conforme os dados informados (a função att_alunos espera ambos os campos)
            if novo_nome and nova_serie:
                att_alunos(matricula, novo_nome, nova_serie)
            elif novo_nome:
                att_alunos(matricula, novo_nome, None)  # Atualiza apenas o nome
            elif nova_serie:
                att_alunos(matricula, None, nova_serie) # Atualiza apenas a série
            else:
                print("Nenhuma alteração informada.")
        elif opcao == '4':
            matricula = input("Matrícula do aluno para remover: ")
            remove_aluno(matricula)
        elif opcao == '5':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_materias():
    """Menu para gerenciar matérias"""
    while True:
        print("\n--- Gerenciar Matérias ---")
        print("1. Adicionar Matéria")
        print("2. Listar Matérias")
        print("3. Atualizar Matéria")
        print("4. Remover Matéria")
        print("5. Voltar ao menu principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            nome = input("Nome da matéria: ")
            codigo = input("Código da matéria: ")
            add_materia(nome, codigo)
        elif opcao == '2':
            list_materias()
        elif opcao == '3':
            codigo = input("Código da matéria para atualizar: ")
            novo_nome = input("Novo nome da matéria: ")
            att_materias(codigo, novo_nome)
        elif opcao == '4':
            codigo = input("Código da matéria para remover: ")
            remove_materias(codigo)
        elif opcao == '5':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

def menu_notas():
    """Menu para gerenciar notas"""
    while True:
        print("\n--- Gerenciar Notas ---")
        print("1. Adicionar/Atualizar Nota")
        print("2. Gerar Relatório de Aluno")
        print("3. Voltar ao menu principal")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            matricula = input("Matrícula do aluno: ")
            codigo = input("Código da matéria: ")
            trimestre = int(input("Trimestre (1, 2 ou 3): "))
            nota = float(input("Nota: "))
            adicionar_nota(matricula, codigo, trimestre, nota)
        elif opcao == '2':
            matricula = input("Matrícula do aluno para o relatório: ")
            gerar_relatorio_aluno(matricula)
        elif opcao == '3':
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    # Cria o banco de dados e suas tabelas (se ainda não existirem) antes de iniciar o menu
    create_database()
    # Inicia o menu principal do sistema
    menu_principal()
