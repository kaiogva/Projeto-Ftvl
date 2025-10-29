import tkinter as tk
from ui.tela_inicial import TelaInicial
from ui.tela_login import TelaLogin 
from ui.tela_cadastro import TelaCadastro 
from ui.tela_unidades import TelaUnidades 
from ui.tela_agendamento import TelaAgendamento

# Função para alternar telas
def mostrar_tela(nome, unidade=None): # Adicionado parâmetro opcional 'unidade'
    frame = telas[nome]
    
    # Se for a tela de agendamento, chamamos o método para carregar os horários
    if nome == "agendamento" and unidade:
        frame.exibir_horarios(unidade) 
        
    frame.tkraise()

# Janela principal
root = tk.Tk()
root.title("CT Andrade - Futevôlei")
root.geometry("1024x768")
root.configure(bg="#303030")
root.eval('tk::PlaceWindow . center')

# Configurar grade
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Criar frames (telas)
telas = {
    "inicial": TelaInicial(root, mostrar_tela),
    "login": TelaLogin(root, mostrar_tela),
    "cadastro": TelaCadastro(root, mostrar_tela),
    "unidades": TelaUnidades(root, mostrar_tela), 
    "agendamento": TelaAgendamento(root, mostrar_tela)
}

# Posicionar todos os frames
for frame in telas.values():
    frame.grid(row=0, column=0, sticky="nsew")

# Mostrar tela inicial
mostrar_tela("inicial")

# Executar interface
root.mainloop()
