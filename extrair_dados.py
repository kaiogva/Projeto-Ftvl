import mysql.connector 
from getpass import getpass # Recomendado para senhas em script local (melhor que deixar visível)

# 1. Configuração da Conexão
# RECOMENDAÇÃO: NÃO DEIXE A SENHA VISÍVEL NO CÓDIGO FINAL
DB_CONFIG = {
    'user': 'seu_usuario',
    # Você pode pedir a senha de forma segura no console
    # 'password': getpass("Digite sua senha do MySQL: "), 
    'password': 'sua_senha', # SUBSTITUA PELA SUA SENHA REAL
    'host': 'localhost',
    'database': 'seu_banco_de_dados' # SUBSTITUA PELO NOME DO SEU BANCO
}

# 2. Query de Extração
# 🚨 IMPORTANTE: Substitua 'sua_tabela' pelo nome real da sua tabela!
SQL_QUERY = 'SELECT nome, unidade, horario FROM sua_tabela'

def extrair_dados_especificos():
    """Conecta ao MySQL, executa a consulta e retorna os dados de Nome, Unidade e Horario."""
    
    cnx = None
    dados_extraidos = []
    
    try:
        # Tenta estabelecer a conexão
        cnx = mysql.connector.connect(**DB_CONFIG)
        # dictionary=True faz com que os resultados venham como dicionários (chave:nome da coluna)
        cursor = cnx.cursor(dictionary=True) 
        
        # Executa a query
        print(f"Executando a consulta: {SQL_QUERY}...")
        cursor.execute(SQL_QUERY)
        
        # Obtém todos os resultados
        dados_extraidos = cursor.fetchall()
        
        print(f"Extração concluída. {len(dados_extraidos)} registros encontrados.")
        
    except mysql.connector.Error as err:
        print(f"\n🚨 Erro ao extrair dados do MySQL: {err}")
        
    finally:
        # 3. Fechar a conexão
        if cnx and cnx.is_connected():
            cursor.close()
            cnx.close()
            print("Conexão MySQL fechada.")
            
    return dados_extraidos

# --- Execução da Extração ---
resultados = extrair_dados_especificos()

# 4. Exemplo de uso dos dados extraídos
if resultados:
    print("\n--- Dados Extraídos ---")
    for linha in resultados:
        # Acessando os campos solicitados: nome, unidade, horario
        nome = linha.get('nome', 'N/A')
        unidade = linha.get('unidade', 'N/A')
        horario = linha.get('horario', 'N/A')
        
        print(f"Nome: {nome} | Unidade: {unidade} | Horário: {horario}")
        
    # Agora a variável 'resultados' contém todos os dados que você precisa para
    # gerar seu relatório ou fazer outro tipo de processamento.
else:
    print("\nNenhum dado foi extraído ou houve um erro na conexão/query.")