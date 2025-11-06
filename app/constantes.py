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
    estabelecimento (list[str]):
        Lista de tipos de locais que o robô pesquisará no Google Maps.

    arquivo_json (str):
        Caminho base do arquivo JSON onde os resultados coletados serão armazenados.

    arquivo_excel (str):
        Caminho do arquivo Excel gerado a partir dos resultados em JSON.

    arquivo_log (str):
        Caminho do arquivo de log responsável por registrar todas as etapas da execução.

    quantidade_maxima_por_tipo (int):
        Define o número máximo de estabelecimentos coletados por categoria de busca.

    mostrar_tela_navegador (bool):
        Determina se o navegador será exibido visualmente durante a execução
        (True = modo debug visível, False = execução em segundo plano/headless).

    tempo_maximo_espera_por_elemento (int):
        Tempo máximo (em segundos) para aguardar o carregamento de um elemento
        antes de gerar uma exceção de timeout.

    tentativas_maximas (int):
        Número de tentativas de repetição para inicializar o navegador ou executar ações críticas.

Seletores XPath:
    Todos os seletores abaixo são utilizados pelo módulo `use_case.py` para identificar
    e extrair informações de estabelecimentos diretamente da interface do Google Maps.
    Esses caminhos devem ser ajustados conforme a estrutura do DOM do Maps,
    caso o layout seja atualizado no futuro.

    nome_do_estabelecimento (str):
        XPath que identifica o título principal (nome) do estabelecimento aberto no painel lateral.

    tipo_do_estabelecimento (str):
        XPath que localiza o tipo/categoria do estabelecimento (ex: academia, restaurante, etc).

    nota_do_estabelecimento (str):
        XPath que captura a nota de avaliação (ex: 4.8) exibida no painel.

    avaliacoes_do_estabelecimento (str):
        XPath que retorna o número de avaliações registradas pelos usuários.

    endereco_do_estabelecimento (str):
        XPath dinâmico para localizar o botão com o atributo `aria-label="Copiar endereço"`,
        garantindo maior estabilidade em diferentes tipos de painel (academias, restaurantes, etc).
"""

estabelecimento = ["academias", "restaurantes", "sorveterias"]

arquivo_json = "resultados.json"

arquivo_excel = "resultados.xlsx"

arquivo_log = "automação.log"

quantidade_maxima_por_tipo = 10

mostrar_tela_navegador = True

tempo_maximo_espera_por_elemento = 10

tentativas_maximas = 3

# ----------------------------
# Caminhos (XPath) dos elementos
# ----------------------------

nome_do_estabelecimento = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1'

tipo_do_estabelecimento = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/span[1]/span/button'

nota_do_estabelecimento = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]'

avaliacoes_do_estabelecimento = '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span'

endereco_do_estabelecimento = [
    '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[7]/div[3]/button/div/div[2]/div[1]',
    '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[3]/button/div/div[2]/div[1]',
    '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[11]/div[3]/button/div/div[2]/div[1]'
]