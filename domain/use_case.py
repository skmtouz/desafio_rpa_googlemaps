from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app.constantes import quantidade_maxima_por_tipo, tentativas_maximas, nome_do_estabelecimento, tipo_do_estabelecimento, nota_do_estabelecimento, avaliacoes_do_estabelecimento, endereco_do_estabelecimento
from infra.file_provider import gerar_arquivo_json, gerar_arquivo_excel
from app.utils import get_elemento, scroll_to_element, abrir_navegador, navegar_para_url, fechar_navegador
import logging

def buscar_informacoes(estabelecimento):
    """
    Função principal para buscar e coletar informações no Google Maps.
    - Pesquisa o tipo de estabelecimento (ex: academias)
    - Clica em cada card da lista lateral
    - Aguarda painel lateral abrir (mudança de URL)
    - Extrai os dados com XPaths fixos
    - Fecha o painel e volta para a lista
    - Repete até atingir o limite configurado
    """

    logging.info(f"Iniciando coleta de informações para o estabelecimento: {estabelecimento}")

    resultados = []

    driver = abrir_navegador()

    try:
        navegar_para_url(driver, "https://www.google.com/maps")

        pesquisar_por_estabelecimento_no_maps(driver, estabelecimento)

        indices_cards = gerar_indices_cards(quantidade_maxima_por_tipo)

        for indice in indices_cards:
            try:

                logging.info(f"Processando card com indice: {indice}.")

                selecionar_card_de_estabelecimento(driver, indice)

                avaliacoes, endereco, nome, nota, tipo = extrair_dados_do_card_de_estabelecimento(driver, indice)

                logging.debug(f"armazenando resultados do estabelecimento #{nome} em um item na lista de variaveis.")
                resultados.append({
                    "nome": nome,
                    "tipo": tipo,
                    "nota": nota,
                    "avaliacoes": avaliacoes,
                    "endereco": endereco
                })

                fechar_card_de_estabelecimento(driver, indice)

            except Exception as e:
                logging.error(f"Erro no card #{indice}: {e}")
                continue

        if resultados is None or len(resultados) == 0:
            logging.warning(f"Nenhum resultado coletado para '{estabelecimento}'.")
            return

        gerar_arquivo_json(estabelecimento.lower(), resultados)
        gerar_arquivo_excel(estabelecimento.lower())
        

        #TODO: melhorar essa documentação dessa classe

        #TODO: criar uma pasta de arquivos

        #TODO: conferir as documentações e logs (se são uteis, se precisa adicionar e o nível do LOG)

        #TODO: fazer o Readme

        #TODO: ver se utilizamos pythonPackge ou pastas (eu acho melhor pythonPackage, pastas seria para os arquivos)

    except Exception as erro:
        logging.critical(f"Erro inesperado: {erro}")

    finally:
        fechar_navegador(driver)

def fechar_card_de_estabelecimento(driver, indice):
    """
    Fecha o card de um estabelecimento aberto no Google Maps.

    Essa função identifica e clica no botão de fechamento do card de detalhes de um estabelecimento.
    É utilizada após a extração dos dados do estabelecimento para retornar à lista principal de resultados.

    Args:
        driver (webdriver): Instância ativa do navegador controlada pelo Selenium WebDriver.
        indice (int): Índice do card atualmente aberto, usado apenas para fins de log e rastreamento.
    """
    logging.debug(f"Fechando o card com indice: #{indice}.")
    botao_de_fechar_card = get_elemento(driver, By.XPATH,
                                        '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div/div[3]/span/button')

    botao_de_fechar_card.click()
    logging.debug(f"Card do estabelecimento #{indice} fechado com sucesso.")


def extrair_dados_do_card_de_estabelecimento(driver, indice):
    """
    Extrai informações detalhadas de um card de estabelecimento aberto no Google Maps.

    Essa função coleta os principais dados exibidos na seção de detalhes de um estabelecimento
    (como nome, tipo, nota, número de avaliações e endereço), utilizando seletores XPath
    específicos para cada campo. Os dados são extraídos diretamente do DOM e retornados
    como strings limpas (sem espaços extras).

    Args:
        driver (WebDriver): Instância ativa do Selenium WebDriver.
        indice (int): Índice do card atualmente aberto (usado apenas para logs e rastreabilidade).

    Returns:
        tuple: Uma tupla contendo as seguintes informações, nesta ordem:
            - avaliacoes (str): Texto com o número de avaliações do estabelecimento.
            - endereco (str): Endereço completo conforme exibido no Google Maps.
            - nome (str): Nome do estabelecimento.
            - nota (str): Nota média do estabelecimento (ex: "4,5").
            - tipo (str): Categoria do local (ex: "Academia", "Restaurante", "Sorveteria").
    """
    logging.debug(f"Iniciando extração dos dados do estabelecimento com índice #{indice}.")

    logging.debug(f"recuperando nome do estabelecimento com indice: #{indice}.")
    nome = get_elemento(driver, By.XPATH, nome_do_estabelecimento).text.strip()

    logging.debug(f"recuperando tipo do estabelecimento com indice: #{indice}.")
    tipo = get_elemento(driver, By.XPATH, tipo_do_estabelecimento).text.strip()

    logging.debug(f"recuperando nota do estabelecimento com indice: #{indice}.")
    nota = get_elemento(driver, By.XPATH, nota_do_estabelecimento).text.strip()

    logging.debug(f"recuperando avaliações do estabelecimento com indice: #{indice}.")
    avaliacoes = get_elemento(driver, By.XPATH, avaliacoes_do_estabelecimento).text.strip()

    logging.debug(f"recuperando endereço do estabelecimento com indice: #{indice}.")
    endereco = ""
    for xpath in endereco_do_estabelecimento:
        try:
            elemento = get_elemento(driver, By.XPATH, xpath, tempo=1)
            endereco = elemento.text.strip()

            if endereco:
                logging.debug(f"Endereço encontrado com XPath alternativo: {xpath}")
                break

        except Exception as e:
            logging.debug(f"Tentativa falhou com XPath '{xpath}': {e}")
            continue

    if not endereco:
        logging.error(f"Nenhum endereço encontrado para o card #{indice}.")

    logging.debug(f"Extração concluída com sucesso para o card #{indice}: {nome} ({tipo}).")

    return avaliacoes, endereco, nome, nota, tipo


def selecionar_card_de_estabelecimento(driver, indice):
    """
    Seleciona um card de estabelecimento no Google Maps com múltiplas tentativas de fallback.

    Essa função tenta localizar, rolar até e clicar em um card específico dentro da lista de
    resultados exibidos no painel lateral do Google Maps. Após o clique, valida se o card
    foi realmente aberto com sucesso, garantindo resiliência contra problemas de carregamento
    dinâmico da página (ex: `ElementNotInteractableException`, `StaleElementReferenceException`, etc.).

    O processo é repetido até o número máximo de tentativas definido por `tentativas_maximas`.
    Caso todas falhem, uma exceção é lançada e registrada no log.

    Args:
        driver (WebDriver): Instância ativa do Selenium WebDriver.
        indice (int): Índice do card na lista lateral de resultados do Maps (inicia em 1).

    Raises:
        Exception: Se o card não for aberto com sucesso após `tentativas_maximas` tentativas.

    Notes:
        - O XPath do card é construído dinamicamente com base no índice informado.
        - A função `scroll_to_element()` é usada para garantir que o card esteja visível antes do clique.
        - Após o clique, a presença de um elemento específico na seção de detalhes é usada como validação de sucesso.
    """
    for tentativa in range(1, tentativas_maximas + 1):
        try:
            card = get_elemento(driver, By.XPATH,
                                f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{indice}]/div/a')

            logging.debug(f"Tentativa {tentativa}/{tentativas_maximas} para selecionar o card #{indice}.")

            scroll_to_element(card, driver)

            card.click()

            logging.debug(f"Card #{indice} clicado com sucesso. Validando abertura...")

            get_elemento(driver, By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]')

            logging.debug(f"Card #{indice} aberto e validado com sucesso na tentativa {tentativa}.")

        except Exception as e:
            logging.warning(f"Falha ao abrir o card #{indice} na tentativa {tentativa}: {e}")
            if tentativa > tentativas_maximas:
                logging.error(
                    f"Não foi possível abrir o card #{indice} após {tentativas_maximas} tentativas."
                )
                raise Exception(f"Falha ao abrir o card #{indice} após {tentativas_maximas} tentativas.") from e


def pesquisar_por_estabelecimento_no_maps(driver, estabelecimento):
    """
    Realiza uma busca por um estabelecimento no Google Maps utilizando o campo de pesquisa.

    Essa função localiza a barra de pesquisa na interface do Google Maps, insere o nome do
    estabelecimento desejado e executa a busca pressionando `ENTER`. É usada como ponto
    inicial para coletar resultados ou interagir com locais específicos na página.

    Args:
        driver (WebDriver): Instância ativa do Selenium WebDriver.
        estabelecimento (str): Nome do estabelecimento a ser pesquisado (ex: "Smart Fit", "Outback").
    """
    logging.info(f"Iniciando busca no Google Maps por: '{estabelecimento}'.")

    barra_pesquisa = get_elemento(driver, By.ID, "searchboxinput")

    barra_pesquisa.clear()
    barra_pesquisa.send_keys(estabelecimento)
    barra_pesquisa.send_keys(Keys.ENTER)

    logging.debug(f"Termo '{estabelecimento}' enviado com sucesso para a barra de pesquisa.")


def gerar_indices_cards(quantidade: int) -> List[int]:
    """
    Gera uma lista de índices numéricos para seleção de elementos em sequência.

    A função cria uma lista de números ímpares começando em 3, com espaçamento de 2 em 2,
    até atingir o limite baseado em `quantidade`. Isso é útil em cenários
    onde os elementos de interesse aparecem em posições alternadas, como listas de cards
    HTML onde apenas índices ímpares contêm dados relevantes.

    Args:
        quantidade (int): Quantidade máxima de elementos a serem considerados.

    Returns:
        List[int]: Lista de índices gerados no formato [3, 5, 7, 9, ...].

    Raises:
        ValueError: Se `quantidade` for menor ou igual a zero.

    Notes:
        - O intervalo é calculado como `range(3, (quantidade * 2) + 3, 2)`.
        - O valor final de `range` é exclusivo, por isso o `+3` no limite superior.
    """
    if quantidade <= 0:
        logging.critical("Quantidade inválida: %s. O valor deve ser maior que zero.", quantidade)
        raise ValueError("A quantidade máxima por tipo deve ser maior que zero.")

    logging.debug("Iniciando geração de índices para %d elementos.", quantidade)

    indices = list(range(3, (quantidade * 2) + 3, 2))

    logging.debug("Índices gerados: %s", indices)

    return indices