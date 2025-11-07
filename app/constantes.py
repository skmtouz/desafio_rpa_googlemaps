"""
Módulo: constantes
------------------
Centraliza todas as configurações, parâmetros globais e seletores XPath utilizados na automação
com Selenium. Este arquivo permite controle total do comportamento do robô sem modificar o
código principal, facilitando manutenção, testes e depuração.

Finalidade:
    Este módulo serve como ponto único de configuração do projeto, garantindo que mudanças
    operacionais possam ser feitas de forma simples e segura — por exemplo, ajustando tempos
    de espera, caminhos de arquivos ou seletores de elementos da interface do Google Maps.

Atenção:
    - Evite alterar nomes de variáveis; modifique apenas seus valores.
    - Verifique se os caminhos informados possuem permissões adequadas de leitura e escrita.
    - Todas as constantes aqui definidas são consideradas imutáveis em tempo de execução.
    - O uso centralizado garante consistência entre diferentes módulos (utils, use_case, logs, etc).

Constantes principais:
    url_google_maps (str):
        URL base do Google Maps utilizada na automação.

    estabelecimentos (list[str]):
        Lista de tipos de locais que o robô pesquisará no Google Maps.

    caminho_arquivos (str):
        Caminho base de onde os arquivos gerados serão armazenados.

    nome_arquivo_de_log (str):
        Nome do arquivo de log responsável por registrar todas as etapas da execução.

    quantidade_de_resultados (int):
        Define o número máximo de estabelecimentos coletados por categoria de busca.

    mostrar_tela_navegador (bool):
        Determina se o navegador será exibido visualmente durante a execução
        (True = modo debug visível, False = execução em segundo plano/headless).

    tempo_maximo_espera_por_elemento (int):
        Tempo máximo (em segundos) para aguardar o carregamento de um elemento
        antes de gerar uma exceção de timeout.

    tentativas_maximas (int):
        Número de tentativas de repetição para inicializar o navegador ou executar ações críticas.

    preferencia_de_navegadores (list[str]):
        Lista de navegadores para execução do RPA.

Seletores XPath:
    Todos os seletores abaixo são utilizados pelo módulo `use_case.py` para identificar
    e extrair informações de estabelecimentos diretamente da interface do Google Maps.
    Esses caminhos devem ser ajustados conforme a estrutura do DOM do Maps,
    caso o layout seja atualizado no futuro.

    xpath_nome_do_estabelecimento (str):
        XPath que identifica o título principal (nome) do estabelecimento aberto no painel lateral.

    xpath_tipo_do_estabelecimento (str):
        XPath que localiza o tipo/categoria do estabelecimento (ex: academia, restaurante, etc).

    xpath_nota_do_estabelecimento (str):
        XPath que captura a nota de avaliação (ex: 4.8) exibida no painel.

    xpath_avaliacoes_do_estabelecimento (str):
        XPath que retorna o número de avaliações registradas pelos usuários.

    xpath_endereco_do_estabelecimento (list[str]):
        Lista de XPaths alternativos usados para capturar o endereço completo do estabelecimento
        no painel lateral do Google Maps.

        Essa abordagem garante maior compatibilidade entre diferentes layouts de painéis — 
        como academias, restaurantes e sorveterias — que podem renderizar o endereço em posições
        distintas dentro do DOM. O robô tentará localizar o endereço utilizando os caminhos
        fornecidos, em ordem de prioridade, até encontrar o elemento válido.

    xpath_botao_de_fechar_card (str):
        XPath do botão de fechar o card do estabelecimento.

    xpath_card_completo (str):
        XPath do container principal que contém todas as informações visíveis do card.
"""

url_google_maps = "https://www.google.com/maps"

estabelecimentos = ["academias", "restaurantes", "sorveterias"]

caminho_arquivos = "arquivos_gerados/"

nome_arquivo_de_log = "automação.log"

quantidade_de_resultados = 5

mostrar_tela_navegador = True

tempo_maximo_espera_por_elemento = 10

tentativas_maximas = 3

preferencia_de_navegadores = ['chrome', 'edge', 'firefox']

# ----------------------------
# Caminhos (XPath) dos elementos
# ----------------------------

xpath_nome_do_estabelecimento = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1'

xpath_tipo_do_estabelecimento = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/span[1]/span/button'

xpath_nota_do_estabelecimento = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]'

xpath_avaliacoes_do_estabelecimento = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span'

xpath_endereco_do_estabelecimento = [
    '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[3]/button/div/div[2]/div[1]',
    '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[3]/button/div/div[2]/div[1]',
    '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[11]/div[3]/button/div/div[2]/div[1]'
]

xpath_botao_de_fechar_card = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div/div[3]/span/button'

xpath_card_completo = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]'