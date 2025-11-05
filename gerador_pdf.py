import sqlite3
from fpdf import FPDF
import tkinter as tk
from tkinter import messagebox

# Função para gerar PDF
def gerar_pdf():
    # Conecta ao banco
    conn = sqlite3.connect("ct_futevôlei.db")
    cursor = conn.cursor()

    # 1. Selecionar TODAS as colunas que serão usadas no PDF.
    cursor.execute("SELECT id, nome, email, unidade, dia_semana, horario FROM alunos")
    dados = cursor.fetchall()
    conn.close()

    if not dados:
        messagebox.showwarning("Aviso", "Nenhum dado encontrado no banco!")
        return

    # Cria PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Lista de Usuários", ln=True, align="C")

    # Cabeçalho da tabela (Ajustando larguras para caber na página A4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(10, 10, "id".upper(), border=1)
    pdf.cell(25, 10, "nome".upper(), border=1)
    pdf.cell(50, 10, "email".upper(), border=1) # Largura ajustada
    pdf.cell(35, 10, "unidade".upper(), border=1)
    pdf.cell(15, 10, "dia".upper(), border=1)
    pdf.cell(23, 10, "horario".upper(), border=1)
    pdf.ln()

    # Dados da tabela
    pdf.set_font("Arial", "", 12)
    for linha in dados:
        # 2. Corrigindo índices (0 a 5) E tratando o erro 'NoneType' com 'if linha[x] is not None else ""'
        
        # O str() é necessário apenas para o id, que é um número.
        id_seguro = str(linha[0]) if linha[0] is not None else "" 
        
        # Demais colunas (Strings)
        nome_seguro = linha[1] if linha[1] is not None else ""
        email_seguro = linha[2] if linha[2] is not None else ""
        unidade_segura = linha[3] if linha[3] is not None else ""
        dia_semana_seguro = linha[4] if linha[4] is not None else ""
        horario_seguro = linha[5] if linha[5] is not None else ""

        pdf.cell(10, 10, id_seguro, border=1)
        pdf.cell(25, 10, nome_seguro, border=1)
        pdf.cell(50, 10, email_seguro, border=1)
        pdf.cell(35, 10, unidade_segura, border=1)
        pdf.cell(15, 10, dia_semana_seguro, border=1)
        pdf.cell(23, 10, horario_seguro, border=1)
        
        pdf.ln()

    # Salva PDF
    pdf.output("usuarios.pdf")
    messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")

# Cria interface Tkinter (Mantida)
root = tk.Tk()
root.title("Gerar PDF do Banco de Dados")
root.geometry("300x150")

# Botão
botao = tk.Button(root, text="Gerar PDF", command=gerar_pdf, font=("Arial", 12), bg="#4CAF50", fg="white")
botao.pack(pady=40)

root.mainloop()