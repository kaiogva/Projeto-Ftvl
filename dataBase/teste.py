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
        """Cria a tabela 'alunos' se ela ainda não existir."""
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


    # 2. Adiciona a nova coluna 'senha' (TEXT) se ela não existir
        try:
            # O comando ALTER TABLE ADD COLUMN é a forma correta de adicionar colunas.
            # O SQLite tentará executar este comando, e se a coluna já existir,
            # ele lançará um erro, que será pego pelo 'except'.
            self.tabela.execute("ALTER TABLE alunos ADD COLUMN senha TEXT")
            # Salva a alteração da estrutura da tabela
            self.conexao.commit() 
            print("Coluna 'senha' adicionada à tabela 'alunos'.")
        except sqlite3.OperationalError as e:
            # Erro comum: 'duplicate column name: senha'
            if "duplicate column name" in str(e):
                pass # A coluna já existe, apenas ignoramos.
            else:
                # Outro erro inesperado
                print(f"Erro ao adicionar coluna 'senha': {e}")
        
        # Não precisa do self.conexao.commit() aqui se o 'ALTER TABLE' já fez um.


    def inserir_aluno(self, nome, email, senha, idade=None, telefone=None, plano=None):
            """Insere um novo registro de aluno no banco de dados, incluindo a senha."""
            # ... (As verificações de obrigatoriedade estão OK) ...

            data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # 1. Inclua 'senha' na lista de COLUNAS
                # 2. Use 7 placeholders (?) para 7 valores (incluindo 'senha')
                self.tabela.execute("""INSERT INTO alunos (nome, idade, telefone, email, plano, senha, data_cadastro)
                                VALUES (?, ?, ?, ?, ?, ?, ?)""", # 7 placeholders
                            # 3. Inclua 'senha' na tupla de VALORES, antes de data_cadastro
                            (nome, idade, telefone, email, plano, senha, data_cadastro))
                self.conexao.commit()
                return True, "Aluno cadastrado com sucesso!"
            except sqlite3.Error as e:
                return False, f"Erro de DB: {e}"

    # NO SEU ARQUIVO DBManager (ou sqlite_service.py)

# ... (restante da classe DBManager) ...

    def verificar_login(self, email, senha):
        """Busca um aluno pelo email e verifica a senha."""
        try:
            self.tabela.execute("SELECT nome, senha FROM alunos WHERE email = ?", (email,))
            aluno = self.tabela.fetchone()
            
            if aluno is None:
                return False, "E-mail não encontrado."
            
            # O fetchone retorna uma tupla (nome, senha)
            nome, senha_armazenada = aluno 
            
            # Verificação da senha
            if senha == senha_armazenada:
                return True, nome  # Retorna sucesso e o nome do aluno
            else:
                return False, "Senha incorreta."
                
        except sqlite3.Error as e:
            return False, f"Erro de DB ao verificar login: {e}"

# ... (restante da classe DBManager) ...

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conexao.close()
        # print(f"Conexão com {DB_NAME} fechada.")

# Você pode manter suas outras funções (listar, atualizar, deletar) aqui
# e o loop do menu (while True) se for necessário para um modo de console.
# Contudo, para o Tkinter, só precisaremos da função de inserção e da conexão.