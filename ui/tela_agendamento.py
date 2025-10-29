import tkinter as tk
from tkinter import ttk
from ui.dados_agendamento import AGENDAMENTOS
from tkinter import messagebox
# Importe suas variáveis de cores
from assets.cores import * # Ajuste este caminho conforme necessário

# Variáveis de Estilo
BUTTON_WIDTH_HORARIO = 8 # Um tamanho um pouco menor para o botão de horário

class TelaAgendamento(tk.Frame):
    def __init__(self, master, mudar_tela_callback):
        # ----------------------------------------------------------------------
        # ALTERAÇÃO: Fundo da tela principal
        # ----------------------------------------------------------------------
        super().__init__(master, bg=cor_de_fundo, width=1024, height=768)
        self.master = master
        self.mudar_tela = mudar_tela_callback
        self.pack_propagate(False)
        
        self.unidade_selecionada = None 

        # Frame principal para os horários (usaremos para limpar e reconstruir)
        # ----------------------------------------------------------------------
        # ALTERAÇÃO: Fundo do container principal
        # ----------------------------------------------------------------------
        self.horarios_container = tk.Frame(self, bg=cor_de_fundo, padx=40, pady=20)
        self.horarios_container.pack(fill="both", expand=True)

        # Título da tela (será atualizado dinamicamente)
        # ----------------------------------------------------------------------
        # ALTERAÇÃO: Fundo e Cor da Fonte do Título
        # ----------------------------------------------------------------------
        self.titulo_unidade = tk.Label(self.horarios_container, text="Selecione uma Unidade", 
                                       font=("Arial", 20, "bold"), bg=cor_de_fundo, fg="white")
        self.titulo_unidade.pack(pady=20)
        
        # ----------------------------------------------------------------------
        # ALTERAÇÃO: Botão para voltar (Estilo: Criar Conta - cor_botao_registrar)
        # ----------------------------------------------------------------------
        tk.Button(
            self.horarios_container, 
            text="< Voltar às Unidades", 
            command=lambda: self.mudar_tela("unidades"),
            font=("Arial", 12),
            bg=cor_botao_registrar,
            fg="white", 
            relief="flat",
            borderwidth=0,
            highlightthickness=2,
            highlightbackground="white",
            activebackground="#404040",
            padx=10,
            pady=5
        ).pack(pady=10, anchor='w')

    def exibir_horarios(self, unidade):
        print(f"DEBUG: Iniciando exibição para unidade: {unidade}")

        """Preenche a tela com os horários da unidade selecionada."""
        self.unidade_selecionada = unidade
        self.titulo_unidade.config(text=f"Agendamento - Unidade {unidade}")

        # 1. Limpa o conteúdo anterior 
        for widget in self.horarios_container.winfo_children()[2:]:
            widget.destroy()

        # 2. Obtém os dados
        dados_horarios = AGENDAMENTOS.get(unidade, {})

        # 3. Cria a área de scroll (ideal para muitas opções)
        # ----------------------------------------------------------------------
        # ALTERAÇÃO: Fundo do Canvas e Frame Interno
        # ----------------------------------------------------------------------
        canvas = tk.Canvas(self.horarios_container, bg=cor_de_fundo, highlightthickness=0) # Removendo a borda padrão
        scroll_y = tk.Scrollbar(self.horarios_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=cor_de_fundo, padx=10, pady=10)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20) # Adicionei um padx aqui
        scroll_y.pack(side="right", fill="y")
        
        # Título "Horários Livres:" (baseado na primeira imagem)
        tk.Label(scrollable_frame, text="Horários Livres:", font=("Arial", 16, "bold"), 
                 bg=cor_de_fundo, fg="white").pack(anchor='w', pady=(0, 20))


        # 4. Itera e constrói a UI
        for dia, horarios in dados_horarios.items():
            # Título do Dia
            tk.Label(scrollable_frame, text=dia, font=('Arial', 12, 'bold'), 
                      bg=cor_de_fundo, fg='white').pack(anchor='w', pady=(15, 5))

            # Frame para os botões de horário em linha
            # ----------------------------------------------------------------------
            # ALTERAÇÃO: Usando tk.Frame
            # ----------------------------------------------------------------------
            horario_row_frame = tk.Frame(scrollable_frame, bg=cor_de_fundo)
            horario_row_frame.pack(anchor='w', fill='x')

            for horario in horarios:
                # ----------------------------------------------------------------------
                # ALTERAÇÃO: Estilizando Botões de Horário (Cor: cor_destaque)
                # ----------------------------------------------------------------------
                tk.Button(
                    horario_row_frame,
                    text=horario,
                    command=lambda h=horario, d=dia: self.confirmar_agendamento(d, h),
                    font=("Arial", 12, "bold"),
                    width=BUTTON_WIDTH_HORARIO,
                    bg=cor_destaque,
                    fg="white",
                    relief="flat",
                    borderwidth=0,
                    padx=10,
                    pady=5
                ).pack(side="left", padx=5, pady=5)


    def confirmar_agendamento(self, dia, horario):
        """Lógica para finalizar o agendamento."""
        messagebox.showinfo("Agendamento", 
                               f"Agendamento Confirmado!\nUnidade: {self.unidade_selecionada}\nDia: {dia}\nHorário: {horario}")
        # Lógica de persistência (DB, arquivo, etc.) entraria aqui.