from fpdf import FPDF
from datetime import datetime
import os 

class GeradorPDF(FPDF):
    """Classe customizada para gerar o relatório de agendamentos."""
    
    def header(self):
        # Título
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, self.encode_str('Relatório de Agendamentos - CT Futevôlei'), 0, 1, 'C') 
        self.set_font('Arial', '', 10)
        self.cell(0, 5, self.encode_str(f'Gerado em: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'), 0, 1, 'C')
        self.ln(5)

    def footer(self):
        # Número da página
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, self.encode_str(f'Página {self.page_no()}'), 0, 0, 'C')

    def encode_str(self, text):
        """Codifica o texto para evitar problemas com acentuação no fpdf."""
        return str(text).encode('latin-1', 'replace').decode('latin-1')

    def print_agendamentos(self, dados, cabecalho):
        # Larguras ajustadas para os 4 campos: Nome, Unidade, Dia, Horário
        col_widths = [60, 50, 40, 40] 
        
        # Configuração da Fonte e Cor para o CABEÇALHO
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(173, 216, 230) 
        
        # CABEÇALHO da Tabela
        for i, header in enumerate(cabecalho):
            self.cell(col_widths[i], 7, self.encode_str(header), 1, 0, 'C', True)
        self.ln() 
        
        # Linhas da Tabela
        self.set_font('Arial', '', 10)
        fill = False 
        
        for row in dados:
            if fill:
                 self.set_fill_color(240, 240, 240) 
            else:
                 self.set_fill_color(255, 255, 255) 
            
            for i, data in enumerate(row):
                self.cell(col_widths[i], 6, self.encode_str(str(data)), 1, 0, 'L', fill)
            self.ln()
            
            fill = not fill 

def gerar_pdf_agendamentos(db_manager):
    """Função principal para gerar o PDF a partir dos dados do DB."""
    
    dados, cabecalho = db_manager.obter_dados_agendamentos_para_pdf()
    
    if not dados:
        return False, "Nenhum agendamento encontrado para gerar o relatório."

    pdf = GeradorPDF(orientation='P', unit='mm', format='A4') 
    pdf.alias_nb_pages()
    pdf.add_page()
    
    pdf.print_agendamentos(dados, cabecalho)
    
    # Define o nome do arquivo no diretório atual
    nome_arquivo = f"relatorio_agendamentos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    caminho_completo = os.path.join(os.getcwd(), nome_arquivo)

    try:
        pdf.output(caminho_completo, 'F') 
        return True, f"PDF gerado com sucesso!\nArquivo: {nome_arquivo}"
    except Exception as e:
        return False, f"Erro ao salvar PDF: {e}"