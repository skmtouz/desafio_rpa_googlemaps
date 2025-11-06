"""
Módulo: constants
-----------------
Define as configurações globais e parâmetros ajustáveis do projeto de automação com Selenium.

Este arquivo centraliza todas as variáveis de configuração que controlam o comportamento do robô,
permitindo ajustes rápidos sem modificar o código principal. É ideal para facilitar manutenção,
debug e parametrização do ambiente de execução.

Atenção:
    - Evite alterar nomes de variáveis, apenas seus valores.
    - Para mudanças sensíveis (como caminhos de arquivos), verifique permissões e diretórios.
    - Todas as variáveis são consideradas constantes (não devem ser modificadas em tempo de execução).

Constantes:
    estabelecimento (list[str]): Lista de tipos de locais que o robô pesquisará no Google Maps.
    arquivo_json (str): Caminho do arquivo JSON onde os resultados serão armazenados.
    arquivo_excel (str): Caminho do arquivo Excel gerado após a coleta de dados.
    arquivo_log (str): Caminho do arquivo de log com histórico das execuções do robô.
    quantidade_maxima_por_tipo (int): Quantidade máxima de estabelecimentos coletados por categoria.
    mostrar_tela_navegador (bool): Define se o navegador será exibido durante a execução (modo debug).
    tempo_maximo_espera_por_elemento (int): Tempo máximo (em segundos) para esperar elementos carregarem.
    tentativas_maximas (int): Número máximo de tentativas antes de considerar uma ação falha.
"""

# Locais que o robô irá pesquisar no Google Maps.
estabelecimento = ["academias", "restaurantes", "sorveterias"]

# Arquivo onde o robô armazenará os resultados em formato JSON.
arquivo_json = "resultados.json"

# Arquivo Excel que será gerado após a coleta de dados.
arquivo_excel = "resultados.xlsx"

# Arquivo de log que registra todas as operações executadas durante a automação.
arquivo_log = "automação.log"

# Quantidade máxima de estabelecimentos coletados por tipo (limita o volume de resultados).
quantidade_maxima_por_tipo = 15

# Define se o navegador deve ser exibido durante a execução (True = visível, False = oculto).
mostrar_tela_navegador = True

# Tempo máximo (em segundos) para aguardar carregamento de elementos no DOM.
tempo_maximo_espera_por_elemento = 10

# Número máximo de tentativas para executar uma ação antes de falhar.
tentativas_maximas = 3