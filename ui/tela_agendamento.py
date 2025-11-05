import tkinter as tk
from tkinter import messagebox
from assets.cores import *
from dataBase.teste import DBManager  # ajuste conforme seu projeto

# Variáveis de estilo
BUTTON_WIDTH_HORARIO = 8  # tamanho dos botões de horário
db_manager = DBManager()

class TelaAgendamento(tk.Frame):
    def __init__(self, master, mudar_tela_callback):
        super().__init__(master, bg=cor_de_fundo, width=1024, height=768)
        self.master = master
        self.mudar_tela = mudar_tela_callback
        self.pack_propagate(False)
        
        self.unidade_selecionada = None

        # Frame principal para os horários
        self.horarios_container = tk.Frame(self, bg=cor_de_fundo, padx=40, pady=20)
        self.horarios_container.pack(fill="both", expand=True)

        # Título
        self.titulo_unidade = tk.Label(
            self.horarios_container, text="Selecione uma Unidade", 
            font=("Arial", 20, "bold"), bg=cor_de_fundo, fg="white"
        )
        self.titulo_unidade.pack(pady=20)

        # Botão de voltar
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
        """Mostra os horários disponíveis para a unidade."""
        from ui.dados_agendamento import AGENDAMENTOS  # importe aqui para não circular

        self.unidade_selecionada = unidade
        self.titulo_unidade.config(text=f"Agendamento - Unidade {unidade}")

        # Limpa widgets antigos
        for widget in self.horarios_container.winfo_children()[2:]:
            widget.destroy()

        dados_horarios = AGENDAMENTOS.get(unidade, {})

        # Canvas com scroll
        canvas = tk.Canvas(self.horarios_container, bg=cor_de_fundo, highlightthickness=0)
        scroll_y = tk.Scrollbar(self.horarios_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=cor_de_fundo, padx=10, pady=10)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scroll_y.pack(side="right", fill="y")

        # Título dos horários
        tk.Label(
            scrollable_frame, text="Horários Livres:", 
            font=("Arial", 16, "bold"), bg=cor_de_fundo, fg="white"
        ).pack(anchor='w', pady=(0, 20))

        # Cria os botões
        for dia, horarios in dados_horarios.items():
            tk.Label(
                scrollable_frame, text=dia, font=("Arial", 12, "bold"),
                bg=cor_de_fundo, fg='white'
            ).pack(anchor='w', pady=(15, 5))

            row_frame = tk.Frame(scrollable_frame, bg=cor_de_fundo)
            row_frame.pack(anchor='w', fill='x')

            for horario in horarios:
                tk.Button(
                    row_frame,
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
        """Confirma o agendamento e salva no banco de dados."""
        # Verifica se o aluno está logado
        if not hasattr(self.master, "aluno_id") or self.master.aluno_id is None:
            messagebox.showerror("Erro", "Você precisa estar logado para agendar.")
            return

        aluno_id = self.master.aluno_id
        unidade = self.unidade_selecionada

        # Atualiza no banco
        sucesso, msg = self.master.db_manager.atualizar_aluno(
            aluno_id,
            unidade=unidade,
            dia_semana=dia,
            horario=horario
        )

        if sucesso:
            messagebox.showinfo(
                "Agendamento Confirmado",
                f"Agendamento confirmado!\nUnidade: {unidade}\nDia: {dia}\nHorário: {horario}"
            )
        else:
            messagebox.showerror(
                "Erro",
                f"Não foi possível salvar o agendamento:\n{msg}"
            )