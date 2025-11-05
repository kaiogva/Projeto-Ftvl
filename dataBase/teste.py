import sqlite3
from datetime import datetime

DB_NAME = "ct_futevôlei.db"

class DBManager:
    """Gerencia a conexão e operações com o banco de dados SQLite."""

    def __init__(self):
        # Conexão com o banco de dados (será criada se não existir)
        self.conexao = sqlite3.connect(DB_NAME)
        self.tabela = self.conexao.cursor()
        self._criar_tabela()

    def _criar_tabela(self):
        """Cria a tabela 'alunos' e adiciona colunas novas se não existirem."""
        # Criação da tabela principal
        self.tabela.execute("""CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER,
                telefone TEXT,
                email TEXT,
                plano TEXT,
                data_cadastro TEXT NOT NULL
                )""")
        self.conexao.commit()

        # Adiciona coluna 'senha' se não existir
        try:
            self.tabela.execute("ALTER TABLE alunos ADD COLUMN senha TEXT")
            self.conexao.commit()
            print("Coluna 'senha' adicionada à tabela 'alunos'.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                pass
            else:
                print(f"Erro ao adicionar coluna 'senha': {e}")

        # Adiciona colunas 'unidade', 'dia_semana' e 'horario' se não existirem
        for coluna in ["unidade", "dia_semana", "horario"]:
            try:
                self.tabela.execute(f"ALTER TABLE alunos ADD COLUMN {coluna} TEXT")
                self.conexao.commit()
                print(f"Coluna '{coluna}' adicionada à tabela 'alunos'.")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    pass
                else:
                    print(f"Erro ao adicionar coluna '{coluna}': {e}")

    def inserir_aluno(self, nome, email, senha, idade=None, telefone=None, plano=None,
                      unidade=None, dia_semana=None, horario=None):
        """Insere um novo aluno no banco, incluindo todos os campos."""
        data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            self.tabela.execute("""INSERT INTO alunos 
                (nome, idade, telefone, email, plano, senha, data_cadastro, unidade, dia_semana, horario)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (nome, idade, telefone, email, plano, senha, data_cadastro, unidade, dia_semana, horario)
            )
            self.conexao.commit()
            return True, "Aluno cadastrado com sucesso!"
        except sqlite3.Error as e:
            return False, f"Erro de DB: {e}"

    def verificar_login(self, email, senha):
        try:
            self.tabela.execute("SELECT id, nome, senha, unidade, dia_semana, horario FROM alunos WHERE email = ?", (email,))
            aluno = self.tabela.fetchone()
        
            if aluno is None:
                return False, "E-mail não encontrado."
        
            aluno_id, nome, senha_armazenada, unidade, dia_semana, horario = aluno
        
            if senha == senha_armazenada:
                 return True, {
                    "id": aluno_id,
                    "nome": nome,
                    "unidade": unidade,
                    "dia_semana": dia_semana,
                    "horario": horario
                }
            else:
                return False, "Senha incorreta."
            
        except sqlite3.Error as e:
                return False, f"Erro de DB ao verificar login: {e}"

    def atualizar_aluno(self, aluno_id, **kwargs):
        """Atualiza campos do aluno (nome, idade, telefone, plano, unidade, dia_semana, horario)."""
        campos = ", ".join([f"{k} = ?" for k in kwargs.keys()])
        valores = list(kwargs.values())
        valores.append(aluno_id)

        try:
            self.tabela.execute(f"UPDATE alunos SET {campos} WHERE id = ?", valores)
            self.conexao.commit()
            return True, "Aluno atualizado com sucesso!"
        except sqlite3.Error as e:
            return False, f"Erro ao atualizar aluno: {e}"

    def listar_alunos(self):
        """Retorna todos os alunos cadastrados."""
        try:
            self.tabela.execute("SELECT * FROM alunos")
            return self.tabela.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao listar alunos: {e}")
            return []

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conexao.close()