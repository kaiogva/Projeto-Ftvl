import tkinter as tk
from tkinter import messagebox
# Importe sua classe DBManager
from dataBase.teste import DBManager # Ajuste este caminho conforme necessário
from assets.cores import *

# Instancia o gerenciador do banco de dados (Deve ser a mesma instância do seu app principal)
db_manager = DBManager()


class TelaLogin(tk.Frame):
    def __init__(self, master, mudar_tela_callback):
        super().__init__(master, bg=cor_de_fundo, width=1024, height=768)
        self.master = master
        self.mudar_tela = mudar_tela_callback

        self.pack_propagate(False)

        frame_content = tk.Frame(self, bg=cor_de_fundo)
        frame_content.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(frame_content, text="Tela de Login", font=("Arial", 20, "bold", ), bg=cor_de_fundo, fg="white") # <--- AQUI
        label.pack(pady=20)

        # Usaremos 'Email' para a busca, que deve estar no campo 'Usuário'
        tk.Label(frame_content, text="Email:", bg=cor_de_fundo, font=("Arial", 14, ), fg="white").pack(pady=5) # <--- AQUI
        self.entry_email = tk.Entry(frame_content, font=("Arial", 14)) # Renomeei para Email
        self.entry_email.pack(pady=5)

        tk.Label(frame_content, text="Senha:", bg=cor_de_fundo, font=("Arial", 14, ), fg="white").pack(pady=5) # <--- AQUI
        self.entry_pass = tk.Entry(frame_content, show="*", font=("Arial", 14, ))
        self.entry_pass.pack(pady=5)


        frame_botoes = tk.Frame(frame_content, bg=cor_de_fundo)
        frame_botoes.pack(pady=30) 
        

        BUTTON_WIDTH = 16 

        # ----------------------------------------------------------------------
        # 1. Botão INICIAR SESSÃO (Cor: cor_destaque)
        # ----------------------------------------------------------------------
        iniciar_sessao_button = tk.Button(
            frame_botoes, 
            text="ENTRAR", 
            font=("Arial", 14),
            width=BUTTON_WIDTH, 
            bg=cor_destaque,       # CORREÇÃO: Variável de cor passada diretamente
            fg="white", 
            padx=20, 
            pady=10,
            relief="flat",        
            borderwidth=0,        
            command=self.verificar_login
        )
        iniciar_sessao_button.pack(side=tk.LEFT, padx=10)
        
        # ----------------------------------------------------------------------
        # 2. Botão CRIAR CONTA (Cor: cor_botao_registrar)
        # ----------------------------------------------------------------------
        criar_conta_button = tk.Button(
            frame_botoes, 
            text="CRIAR CONTA", 
            font=("Arial", 14),
            width=BUTTON_WIDTH, 
            bg=cor_botao_registrar, # CORREÇÃO: Variável de cor passada diretamente
            fg="white", 
            padx=20, 
            pady=10,
            
            # Estilização para simular a borda branca:
            relief="flat",         
            borderwidth=0,             
            highlightthickness=2,               
            highlightbackground="white",        
            activebackground="#404040",         
            
            command=self.criar_conta 
        )
        criar_conta_button.pack(side=tk.LEFT, padx=10) 

    def iniciar_sessao(self):
        """Redireciona para a tela de Login."""
        print("Botão 'INICIAR SESSÃO' pressionado. Redirecionando para Login.")
        self.mudar_tela("login")

    def criar_conta(self):
        """Redireciona para a tela de Cadastro."""
        print("Botão 'CRIAR CONTA' pressionado. Redirecionando para Cadastro.")
        self.mudar_tela("cadastro")

    # Novo método que será chamado pelo botão ENTRAR
    def verificar_login(self):
        email = self.entry_email.get()
        senha = self.entry_pass.get()

        if not email or not senha:
            messagebox.showwarning("Atenção", "Preencha o e-mail e a senha.")
            return
        
        # Chama o método do DBManager para verificar
        sucesso, resultado = db_manager.verificar_login(email, senha)

        if sucesso:
            nome_usuario = resultado
            messagebox.showinfo("Sucesso", f"Login realizado com sucesso! Bem-vindo(a), {nome_usuario}.")
            # Se o login for válido, chame a função para mudar de tela
            self.mudar_tela("unidades")
        else:
            # resultado será a mensagem de erro ("E-mail não encontrado" ou "Senha incorreta")
            messagebox.showerror("Erro de Login", resultado)


# NOTE: Certifique-se de que no bloco de execução principal (__main__), você também feche a conexão do DB.