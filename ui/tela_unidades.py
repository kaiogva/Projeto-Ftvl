import tkinter as tk
from tkinter import PhotoImage
# Importe suas variáveis de cores
from assets.cores import * # Ajuste este caminho conforme necessário

# Variáveis de Configuração para os Cards
CARD_WIDTH = 350
CARD_HEIGHT = 450
BUTTON_WIDTH = 16 

class TelaUnidades(tk.Frame):
    def __init__(self, master, mudar_tela_callback):
        super().__init__(master, bg=cor_de_fundo, width=1024, height=768)
        self.master = master
        self.mudar_tela = mudar_tela_callback
        self.pack_propagate(False)

        # Título
        titulo = tk.Label(self, text="Escolha a unidade:", font=("Arial", 20, "bold"), 
                          bg=cor_de_fundo, fg="white")
        titulo.pack(pady=40)

        # Frame para os cartões
        cards_frame = tk.Frame(self, bg=cor_de_fundo)
        cards_frame.pack(pady=20)

        # ----------------------------------------------------------------------
        # Cartão Niterói
        # ----------------------------------------------------------------------
        # ALTERAÇÃO: Removendo borda e definindo tamanho fixo
        card_niteroi = tk.Frame(cards_frame, bg=cor_de_fundo, width=CARD_WIDTH, height=CARD_HEIGHT)
        card_niteroi.grid(row=0, column=0, padx=20)
        card_niteroi.pack_propagate(False) # Garante que o Frame mantenha o tamanho fixo

        # Tratamento da imagem (Mantenha o mesmo tamanho da imagem para SG)
        try:
            # Recomenda-se carregar imagens em uma classe principal e passá-las
            self.img_niteroi = PhotoImage(file="assets/capa_NIT.png")
            label_img_niteroi = tk.Label(card_niteroi, image=self.img_niteroi, bg=cor_de_fundo)
            label_img_niteroi.pack(pady=(10, 5))
        except tk.TclError:
            label_img_niteroi = tk.Label(card_niteroi, text="[Imagem NITERÓI]", width=30, height=15, bg="gray")
            label_img_niteroi.pack(pady=(10, 5))

        # Labels internas do card
        label_titulo_niteroi = tk.Label(card_niteroi, text="NITERÓI", font=("Arial", 14, "bold"), bg=cor_de_fundo, fg="white")
        label_titulo_niteroi.pack(pady=5)

        label_end_niteroi = tk.Label(card_niteroi, text="Av. Alm. Ary Parreiras, 20 - Icaraí", font=("Arial", 12), bg=cor_de_fundo, fg="white")
        label_end_niteroi.pack(pady=5)

        # Botão Niterói (Estilo: Botão ENTRAR da Login - cor_destaque e tamanho padrão)
        button_niteroi = tk.Button(
            card_niteroi, 
            text="ACESSE AQUI", 
            font=("Arial", 14),
            width=BUTTON_WIDTH, 
            bg=cor_destaque, 
            fg="white", 
            padx=20, 
            pady=10,
            relief="flat",          
            borderwidth=0,
            command=lambda: self.acessar_unidade("NITERÓI")
        )
        button_niteroi.pack(pady=10)

        # ----------------------------------------------------------------------
        # Cartão São Gonçalo
        # ----------------------------------------------------------------------
       
        card_sg = tk.Frame(cards_frame, bg=cor_de_fundo, width=CARD_WIDTH, height=CARD_HEIGHT)
        card_sg.grid(row=0, column=1, padx=20)
        card_sg.pack_propagate(False) # Garante que o Frame mantenha o tamanho fixo

        # Tratamento da imagem (Mantenha o mesmo tamanho da imagem para NITERÓI)
        try:
            self.img_sg = PhotoImage(file="assets/capa_SG.png")
            label_img_sg = tk.Label(card_sg, image=self.img_sg, bg=cor_de_fundo)
            label_img_sg.pack(pady=(10, 5))
        except tk.TclError:
            label_img_sg = tk.Label(card_sg, text="[Imagem SÃO GONÇALO]", width=30, height=15, bg="gray")
            label_img_sg.pack(pady=(10, 5))

        # Labels internas do card
        label_titulo_sg = tk.Label(card_sg, text="SÃO GONÇALO", font=("Arial", 14, "bold"), bg=cor_de_fundo, fg="white")
        label_titulo_sg.pack(pady=5)

        label_end_sg = tk.Label(card_sg, text="Av. Jorn. Roberto Marinho, 221 - São Gonçalo", font=("Arial", 12), bg=cor_de_fundo, fg="white")
        label_end_sg.pack(pady=5)

        # Botão São Gonçalo (Estilo: Botão ENTRAR da Login - cor_destaque e tamanho padrão)
        button_sg = tk.Button(
            card_sg, 
            text="ACESSE AQUI", 
            font=("Arial", 14),
            width=BUTTON_WIDTH, 
            bg=cor_destaque, 
            fg="white", 
            padx=20, 
            pady=10,
            relief="flat",          
            borderwidth=0,
            command=lambda: self.acessar_unidade("SÃO GONÇALO")
        )
        button_sg.pack(pady=10)

    def acessar_unidade(self, unidade):
        """Passa a unidade selecionada para a função de mudança de tela."""
        print(f"Acessando a unidade: {unidade}")
        self.mudar_tela("agendamento", unidade)