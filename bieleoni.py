import sqlite3

def create_and_populate_db():
    # Conecta ao banco de dados SQLite (ou cria se não existir)
    conn = sqlite3.connect('projeto_python.db')
    cursor = conn.cursor()

    # Criação das tabelas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Aluno (
        Matricula INTEGER PRIMARY KEY,
        Nome TEXT,
        Data_Nascimento DATE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Disciplina (
        ID_Disciplina INTEGER PRIMARY KEY,
        Nome TEXT,
        Professor TEXT,
        Turno TEXT,
        Sala_De_Aula TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Nota (
        Matricula INTEGER NOT NULL,
        ID_Disciplina INTEGER,
        Valor REAL,
        FOREIGN KEY (Matricula) REFERENCES Aluno(Matricula),
        FOREIGN KEY (ID_Disciplina) REFERENCES Disciplina(ID_Disciplina),
        PRIMARY KEY (Matricula, ID_Disciplina)
    );
    ''')

    # Inserção de dados na tabela Aluno
    alunos = [
        (20230004, 'Ana Santos', '2002-03-10'),
        (20230005, 'Pedro Costa', '2000-07-18'),
        (20230006, 'Juliana Almeida', '2001-09-25'),
        (20230007, 'Fernando Ribeiro', '1998-12-05'),
        (20230008, 'Patrícia Nunes', '2003-01-20'),
    ]
    cursor.executemany('INSERT OR IGNORE INTO Aluno (Matricula, Nome, Data_Nascimento) VALUES (?, ?, ?);', alunos)

    # Inserção de dados na tabela Disciplina
    disciplinas = [
        (6721, 'Matemática Avançada', 'Prof. Roberto Almeida', 'Matutino', 'Sala 101'),
        (7654, 'Literatura Brasileira', 'Prof. Ana Lúcia Mendes', 'Vespertino', 'Sala 205'),
        (7641, 'Física Quântica', 'Prof. Carlos Fonseca', 'Noturno', 'Lab. Física 1'),
        (6325, 'Programação em Python', 'Prof. Fernando Costa', 'Noturno', 'Lab. Informática 2'),
        (1344, 'História da Arte', 'Prof. Mariana Santos', 'Vespertino', 'Sala 303'),
    ]
    cursor.executemany('INSERT OR IGNORE INTO Disciplina (ID_Disciplina, Nome, Professor, Turno, Sala_De_Aula) VALUES (?, ?, ?, ?, ?);', disciplinas)

    # Inserção de dados na tabela Nota
    notas = [
        (20230004, 6721, 8.5),
        (20230004, 7641, 7.0),
        (20230005, 7654, 9.0),
        (20230005, 1344, 8.8),
        (20230008, 6325, 6.5),
        (20230008, 7641, 7.5),
        (20230007, 6721, 9.5),
        (20230007, 1344, 8.0),
    ]
    cursor.executemany('INSERT OR IGNORE INTO Nota (Matricula, ID_Disciplina, Valor) VALUES (?, ?, ?);', notas)

    # Commit e fechamento da conexão
    conn.commit()
    conn.close()

def add_aluno():
    conn = sqlite3.connect('projeto_python.db')
    cursor = conn.cursor()
    try:
        matricula = int(input("Digite a matrícula do aluno (número inteiro): "))
        nome = input("Digite o nome do aluno: ").strip()
        data_nascimento = input("Digite a data de nascimento (YYYY-MM-DD): ").strip()
        cursor.execute("INSERT INTO Aluno (Matricula, Nome, Data_Nascimento) VALUES (?, ?, ?);",
                       (matricula, nome, data_nascimento))
        conn.commit()
        print("Aluno adicionado com sucesso.")
    except sqlite3.IntegrityError:
        print("Erro: Matrícula já existe.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

def add_disciplina():
    conn = sqlite3.connect('projeto_python.db')
    cursor = conn.cursor()
    try:
        id_disciplina = int(input("Digite o ID da disciplina (número inteiro): "))
        nome = input("Digite o nome da disciplina: ").strip()
        professor = input("Digite o nome do professor: ").strip()
        turno = input("Digite o turno (Matutino/Vespertino/Noturno): ").strip()
        sala = input("Digite a sala de aula: ").strip()
        cursor.execute("INSERT INTO Disciplina (ID_Disciplina, Nome, Professor, Turno, Sala_De_Aula) VALUES (?, ?, ?, ?, ?);",
                       (id_disciplina, nome, professor, turno, sala))
        conn.commit()
        print("Disciplina adicionada com sucesso.")
    except sqlite3.IntegrityError:
        print("Erro: ID da disciplina já existe.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

def add_nota():
    conn = sqlite3.connect('projeto_python.db')
    cursor = conn.cursor()
    try:
        matricula = int(input("Digite a matrícula do aluno: "))
        id_disciplina = int(input("Digite o ID da disciplina: "))
        valor = float(input("Digite o valor da nota (ex: 8.5): "))
        cursor.execute('''INSERT OR REPLACE INTO Nota (Matricula, ID_Disciplina, Valor)
                          VALUES (?, ?, ?);''', (matricula, id_disciplina, valor))
        conn.commit()
        print("Nota adicionada/atualizada com sucesso.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()

def run_queries():
    conn = sqlite3.connect('projeto_python.db')
    cursor = conn.cursor()

    while True:
        print("\nEscolha uma opção:")
        print("1. Listar Alunos")
        print("2. Listar Disciplinas")
        print("3. Listar Notas")
        print("4. Calcular Média Geral dos Alunos")
        print("5. Calcular Média por Disciplina")
        print("6. Adicionar Aluno")
        print("7. Adicionar Disciplina")
        print("8. Adicionar Nota")
        print("9. Sair")

        choice = input("Digite o número da opção desejada: ")

        if choice == '1':
            cursor.execute('SELECT * FROM Aluno;')
            alunos = cursor.fetchall()
            print("\nLista de Alunos:")
            for aluno in alunos:
                print(f"Matrícula: {aluno[0]}, Nome: {aluno[1]}, Data de Nascimento: {aluno[2]}")

        elif choice == '2':
            cursor.execute('SELECT * FROM Disciplina;')
            disciplinas = cursor.fetchall()
            print("\nLista de Disciplinas:")
            for disciplina in disciplinas:
                print(f"ID: {disciplina[0]}, Nome: {disciplina[1]}, Professor: {disciplina[2]}, Turno: {disciplina[3]}, Sala: {disciplina[4]}")

        elif choice == '3':
            cursor.execute('''
            SELECT a.Nome, d.Nome AS Disciplina, n.Valor AS Nota
            FROM Nota n
            JOIN Aluno a ON n.Matricula = a.Matricula
            JOIN Disciplina d ON n.ID_Disciplina = d.ID_Disciplina;
            ''')
            notas = cursor.fetchall()
            print("\nNotas dos Alunos:")
            for nota in notas:
                print(f"Aluno: {nota[0]}, Disciplina: {nota[1]}, Nota: {nota[2]}")

        elif choice == '4':
            cursor.execute('''
            SELECT a.Nome, AVG(n.Valor) AS Media_Geral
            FROM Nota n
            JOIN Aluno a ON n.Matricula = a.Matricula
            GROUP BY a.Nome;
            ''')
            medias = cursor.fetchall()
            print("\nMédia Geral dos Alunos:")
            for media in medias:
                print(f"Aluno: {media[0]}, Média: {media[1]:.2f}")

        elif choice == '5':
            cursor.execute('''
            SELECT d.Nome AS Disciplina, AVG(n.Valor) AS Media
            FROM Nota n
            JOIN Disciplina d ON n.ID_Disciplina = d.ID_Disciplina
            GROUP BY d.Nome;
            ''')
            medias_disciplinas = cursor.fetchall()
            print("\nMédia por Disciplina:")
            for media in medias_disciplinas:
                print(f"Disciplina: {media[0]}, Média: {media[1]:.2f}")

        elif choice == '6':
            add_aluno()

        elif choice == '7':
            add_disciplina()

        elif choice == '8':
            add_nota()

        elif choice == '9':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

    conn.close()

if __name__ == '__main__':
    create_and_populate_db()
    run_queries()
