import sqlite3
from datetime import datetime

# conexão com o banco de dados
conexao = sqlite3.connect("ct_futevôlei.db")
tabela = conexao.cursor()


# criar tabela de alunos 
tabela.execute("""CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            telefone TEXT,
            email TEXT,
            plano TEXT,
            data_cadastro TEXT NOT NULL
            )""")
conexao.commit()


#  Funções e a Nomenclatura
def cadastrar_aluno():
    print("\n--- Cadastro de Aluno ---")
    nome = input("Nome: ")
    idade = input("Idade: ")
    telefone = input("Telefone: ")
    email = input("Email: ")
    plano = input("Plano (mensal/trimestral/semestral): ")


# Adicionando data de cadastro automaticamente
    data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tabela.execute("""INSERT INTO alunos (nome, idade, telefone, email, plano, data_cadastro)
                      VALUES (?, ?, ?, ?, ?, ?)""",
                   (nome, idade, telefone, email, plano, data_cadastro))
    conexao.commit()
    print("Aluno cadastrado com sucesso!\n")

def listar_alunos():
    print("\n--- Lista de Alunos ---")
    for linha in tabela.execute("SELECT * FROM alunos"):
        print(linha)

def atualizar_aluno():
    listar_alunos()
    aluno_id = input("\nDigite o ID do aluno para atualizar: ")

    nome = input("Novo nome: ")
    idade = input("Nova idade: ")
    telefone = input("Novo telefone: ")
    email = input("Novo email: ")
    plano = input("Novo plano: ")

    tabela.execute("""UPDATE alunos
                      SET nome = ?, idade = ?, telefone = ?, email = ?, plano = ?
                      WHERE id = ?""",
                   (nome, idade, telefone, email, plano, aluno_id))
    conexao.commit()
    print("Dados do aluno atualizados!\n")

def deletar_aluno():
    listar_alunos()
    aluno_id = input("\nDigite o ID do aluno para excluir: ")

    tabela.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
    conexao.commit()
    print("Aluno removido com sucesso!\n")


# Menu principal (painel)
while True:
    print("\n--- Sistema CT Futevôlei ---")
    print("1 - Cadastrar Aluno")
    print("2 - Listar Alunos")
    print("3 - Atualizar Aluno")
    print("4 - Deletar Aluno")
    print("0 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        cadastrar_aluno()
    elif opcao == "2":
        listar_alunos()
    elif opcao == "3":
        atualizar_aluno()
    elif opcao == "4":
        deletar_aluno()
    elif opcao == "0":
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida. Tente novamente.")
