import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox 
# from assets.cores import * # Simulação das variáveis de cor (supondo que vieram daqui)
cor_de_fundo = '#303030'
cor_botao_registrar = '#606060'
cor_destaque = '#F74616'


class TelaInicial(tk.Frame):
    def __init__(self, master, mudar_tela_callback):
        # CORREÇÃO: Removendo as chaves {} e passando a variável de cor diretamente
        super().__init__(master, bg=cor_de_fundo, width=1024, height=768)
        self.master = master
        self.mudar_tela = mudar_tela_callback

        self.pack_propagate(False)
        # CORREÇÃO: Variável de cor passada diretamente
        frame_content = tk.Frame(self, bg=cor_de_fundo) 
        frame_content.place(relx=0.5, rely=0.5, anchor="center")

        # --- Código da Logo e Boas-Vindas (com correções) ---
        logo_path = "assets/Logo.png"
        try:
            self.logo_image = PhotoImage(file=logo_path)
            # CORREÇÃO: Variável de cor passada diretamente
            logo_label = tk.Label(frame_content, image=self.logo_image, bg=cor_de_fundo)
            logo_label.pack(pady=40)
        except tk.TclError:
            # CORREÇÃO: Variável de cor passada diretamente
            logo_label = tk.Label(frame_content, text="[Logo aqui]", font=("Arial", 16), bg=cor_de_fundo, fg="white")
            logo_label.pack(pady=40)
            self.logo_image = None

        # CORREÇÃO: Variável de cor passada diretamente
        welcome_label = tk.Label(frame_content, text="SEJA BEM VINDO", font=("Arial", 16, "bold"), bg=cor_de_fundo, fg="white")
        welcome_label.pack(pady=20)

        # --- NOVO FRAME PARA AGRUPAR OS BOTÕES ---
        # CORREÇÃO: Variável de cor passada diretamente
        frame_botoes = tk.Frame(frame_content, bg=cor_de_fundo)
        frame_botoes.pack(pady=30) 
        
        BUTTON_WIDTH = 16 

        # ----------------------------------------------------------------------
        # 1. Botão INICIAR SESSÃO (Cor: cor_destaque)
        # ----------------------------------------------------------------------
        iniciar_sessao_button = tk.Button(
            frame_botoes, 
            text="INICIAR SESSÃO", 
            font=("Arial", 14),
            width=BUTTON_WIDTH, 
            bg=cor_destaque,       # CORREÇÃO: Variável de cor passada diretamente
            fg="white", 
            padx=20, 
            pady=10,
            relief="flat",        
            borderwidth=0,        
            command=self.iniciar_sessao
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
        
        # --- FIM DO NOVO FRAME ---

    # ... (métodos iniciar_sessao e criar_conta inalterados) ...
    def iniciar_sessao(self):
        """Redireciona para a tela de Login."""
        print("Botão 'INICIAR SESSÃO' pressionado. Redirecionando para Login.")
        self.mudar_tela("login")

    def criar_conta(self):
        """Redireciona para a tela de Cadastro."""
        print("Botão 'CRIAR CONTA' pressionado. Redirecionando para Cadastro.")
        self.mudar_tela("cadastro")


if __name__ == '__main__':
    root = tk.Tk()
    root.title("App Futevôlei")
    root.geometry("1024x768")

    def mock_mudar_tela(tela):
        print(f"Simulando a mudança para a tela: {tela}")

    try:
        from tkinter import ttk
        style = ttk.Style(root)
        style.theme_use('clam')
    except Exception:
        pass
    
    inicial_tela = TelaInicial(root, mock_mudar_tela)
    inicial_tela.pack(fill="both", expand=True)

    root.mainloop()