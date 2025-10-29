import tkinter as tk
from tkinter import messagebox

# Importa a classe do módulo do banco de dados
from dataBase.teste import DBManager
# Importa as cores (necessário para copiar o estilo da TelaLogin)
from assets.cores import * # Ajuste este caminho conforme necessário

# Instancia o gerenciador do banco de dados para ser usado em toda a aplicação
# Idealmente, esta instância deveria ser passada pela classe principal (App)
# para a TelaCadastro, mas para um exemplo rápido, podemos criá-la aqui.
db_manager = DBManager()


class TelaCadastro(tk.Frame):
    def __init__(self, master, mudar_tela_callback):
        # ----------------------------------------------------------------------
        # ALTERAÇÃO: Usando cor_de_fundo da TelaLogin
        # ----------------------------------------------------------------------
        super().__init__(master, bg=cor_de_fundo, width=1024, height=768)
        self.master = master
        self.mudar_tela = mudar_tela_callback

        self.pack_propagate(False)
        
        # ----------------------------------------------------------------------
        # ALTERAÇÃO: Usando cor_de_fundo nos frames internos
        # ----------------------------------------------------------------------
        frame_content = tk.Frame(self, bg=cor_de_fundo)
        frame_content.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(frame_content, text="Cadastro de Usuário", font=("Arial", 20, "bold"), bg=cor_de_fundo, fg="white")
        label.pack(pady=20)

        # Campos de cadastro
        tk.Label(frame_content, text="Nome:", bg=cor_de_fundo, font=("Arial", 14), fg="white").pack(pady=5)
        self.entry_nome = tk.Entry(frame_content, font=("Arial", 14))
        self.entry_nome.pack(pady=5)

        tk.Label(frame_content, text="Email:", bg=cor_de_fundo, font=("Arial", 14), fg="white").pack(pady=5)
        self.entry_email = tk.Entry(frame_content, font=("Arial", 14))
        self.entry_email.pack(pady=5)
        
        tk.Label(frame_content, text="Senha:", bg=cor_de_fundo, font=("Arial", 14), fg="white").pack(pady=5)
        self.entry_senha = tk.Entry(frame_content, show="*", font=("Arial", 14))
        self.entry_senha.pack(pady=5)

        # ----------------------------------------------------------------------
        # ALTERAÇÃO: Novo frame para botões para replicar o layout da Login
        # ----------------------------------------------------------------------
        frame_botoes = tk.Frame(frame_content, bg=cor_de_fundo)
        frame_botoes.pack(pady=30) 

        BUTTON_WIDTH = 16 

        # ----------------------------------------------------------------------
        # 1. Botão CADASTRAR (Estilo: Botão ENTRAR da Login - cor_destaque)
        # ----------------------------------------------------------------------
        cadastrar_button = tk.Button(
            frame_botoes, 
            text="CADASTRAR", 
            font=("Arial", 14),
            width=BUTTON_WIDTH, 
            bg=cor_destaque,       # Cor: cor_destaque (como o ENTRAR)
            fg="white", 
            padx=20, 
            pady=10,
            relief="flat",          # Estilo da Login
            borderwidth=0,          # Estilo da Login
            command=self.cadastrar
        )
        cadastrar_button.pack(side=tk.LEFT, padx=10) # Posicionamento lado a lado

        # ----------------------------------------------------------------------
        # 2. Botão VOLTAR (Estilo: Botão CRIAR CONTA da Login - cor_botao_registrar com borda)
        # ----------------------------------------------------------------------
        back_button = tk.Button(
            frame_botoes, 
            text="VOLTAR", 
            font=("Arial", 14),
            width=BUTTON_WIDTH, 
            bg=cor_botao_registrar, # Cor: cor_botao_registrar
            fg="white", 
            padx=20, 
            pady=10,
            
            # Estilização para simular a borda branca (copiado da TelaLogin):
            relief="flat",  
            borderwidth=0,  
            highlightthickness=2,
            highlightbackground="white", 
            activebackground="#404040", 
            
            command=lambda: self.mudar_tela("login")
        )
        back_button.pack(side=tk.LEFT, padx=10) # Posicionamento lado a lado

    def cadastrar(self):
        nome = self.entry_nome.get()
        email = self.entry_email.get()
        senha = self.entry_senha.get()

        if not nome:
            messagebox.showerror("Erro de Cadastro", "O campo Nome é obrigatório.")
            return
        
        if not email:
            messagebox.showerror("Erro de Cadastro", "O campo Email é obrigatório.")
            return
        
        if not senha:
            messagebox.showerror("Erro de Cadastro", "O campo Senha é obrigatório.")
            return

        # -----------------------------------------------------------
        # CHAMADA AO BANCO DE DADOS ATRAVÉS DA CLASSE IMPORTADA
        # -----------------------------------------------------------
        
        sucesso, mensagem = db_manager.inserir_aluno(
            nome=nome,
            email=email,
            senha=senha,
            # Outros campos da tabela:
            idade=None,
            telefone=None,
            plano=None 
        )

        if sucesso:
            tk.messagebox.showinfo("Cadastro", f"Aluno cadastrado com sucesso! Nome: {nome}")
            # Limpa os campos após o cadastro
            self.entry_nome.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_senha.delete(0, tk.END)
            self.mudar_tela("login")
        else:
            tk.messagebox.showerror("Erro de DB", f"Falha no cadastro: {mensagem}")


# --- Exemplo de Execução (Mantido para testes) ---

if __name__ == "__main__":
    
    try:
        root = tk.Tk()
        root.title("App Futevôlei - Cadastro")
        root.geometry("1024x768")

        def mock_mudar_tela(tela):
            print(f"Simulando a mudança para a tela: {tela}")

        cadastro_tela = TelaCadastro(root, mock_mudar_tela)
        cadastro_tela.pack(fill="both", expand=True)

        root.mainloop()

        # **MUITO IMPORTANTE:** Fechar a conexão quando a aplicação Tkinter terminar.
        db_manager.close()
    except NameError as e:
        print(f"Erro: {e}. Certifique-se de que as variáveis de cor (cor_de_fundo, cor_destaque, etc.) estão definidas em 'assets.cores' ou onde você as importou.")