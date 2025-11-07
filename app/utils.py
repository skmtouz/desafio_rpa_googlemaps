import logging
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.constantes import tempo_maximo_espera_por_elemento, tentativas_maximas, preferencia_de_navegadores, mostrar_tela_navegador
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from app.exceptions import SeleniumError
from time import sleep

def get_elemento(driver, by, seletor, tempo=tempo_maximo_espera_por_elemento):
    """
    Aguarda até que um elemento esteja presente no DOM e o retorna.

    Essa função encapsula a espera explícita do Selenium (`WebDriverWait`)
    para localizar um elemento usando o método de busca informado (ex: By.ID, By.XPATH),
    garantindo que o código só avance quando o elemento realmente existir no DOM.

    Args:
        driver (WebDriver): Instância ativa do Selenium WebDriver.
        by (str): Estratégia de busca (exemplo: `By.ID`, `By.XPATH`, `By.CSS_SELECTOR`).
        seletor (str): Seletor correspondente à estratégia usada.

    Returns:
        WebElement: O elemento encontrado, se presente no DOM dentro do tempo limite.

    Raises:
        SeleniumError: Caso o elemento não seja encontrado dentro do tempo limite
            ou ocorra qualquer outro erro inesperado durante a busca.

    Notes:
        - Esta função apenas verifica a **presença** do elemento no DOM,
          não garante que ele esteja visível ou clicável.
    """
    try:
        logging.debug(
            f"Iniciando busca do elemento com seletor '{seletor}' "
            f"usando método '{by}' (timeout={tempo}s)."
        )

        elemento = WebDriverWait(driver, tempo).until(
            EC.presence_of_element_located((by, seletor))
        )

        logging.debug(f"Elemento encontrado com sucesso: '{seletor}' via '{by}'.")
        return elemento

    except TimeoutException:
        logging.error(f"Timeout: elemento '{seletor}' não encontrado em {tempo}s usando '{by}'.")
        raise SeleniumError(f"Timeout ao localizar o elemento '{seletor}' via '{by}'.")

    except NoSuchElementException:
        logging.error(f"Elemento inexistente no DOM: seletor '{seletor}', método '{by}'.")
        raise SeleniumError(f"Elemento não encontrado: '{seletor}' via '{by}'.")

    except Exception as ex:
        logging.error(f"Erro inesperado ao buscar o elemento '{seletor}' via '{by}': {ex}")
        raise SeleniumError(f"Erro ao buscar o elemento '{seletor}' via '{by}': {ex}")



def scroll_to_element(card, driver):
    """
    Rola a página até que o elemento especificado esteja visível na viewport.

    Essa função utiliza JavaScript para garantir que o elemento HTML passado como
    parâmetro seja trazido para o campo de visão do usuário, permitindo que ele
    seja clicado ou inspecionado visualmente.

    Args:
        card (WebElement): Elemento do Selenium que deve ser rolado até ficar visível.
        driver (WebDriver): Instância ativa do Selenium WebDriver usada para executar o script.

    Raises:
        SeleniumError: Se ocorrer qualquer erro durante a execução do comando JavaScript
            para rolar até o elemento.

    Notes:
        - Equivalente ao método JavaScript ``element.scrollIntoView(true)``.
        - Útil em páginas longas ou quando o Selenium lança exceções
          do tipo ``ElementNotInteractableException`` por o elemento estar fora da viewport.
        - Registra logs de debug antes e depois do scroll, e logs de erro em caso de falha.
    """
    try:
        logging.debug("Iniciando scroll até o elemento: %s", card)
        driver.execute_script("arguments[0].scrollIntoView(true);", card)
        logging.debug("Scroll concluído com sucesso para o elemento: %s", card)
    except Exception as ex:
        logging.error(f"Erro realizar o scroll para o elemento '{card}': {ex}")
        raise SeleniumError(f"Erro ao aguardar o elemento '{card}': {ex}")


def criar_driver(preferencias=preferencia_de_navegadores):
    """
    Cria um WebDriver de acordo com a lista de preferencias.
    preferencias: lista com nomes de navegadores em ordem ex: ['chrome','edge','firefox']

    Retorna: objeto driver (WebDriver) ou None se não conseguiu iniciar nenhum.
    """

    driver = None

    for navegador in preferencias:
        navegador = navegador.lower().strip()
        try:
            logging.info(f"Tentando iniciar o navegador: {navegador}")

            # === GOOGLE CHROME ===
            if navegador == 'chrome':
                opcoes = webdriver.ChromeOptions()
                if not mostrar_tela_navegador:
                    opcoes.add_argument("--headless")

                opcoes.add_argument("--disable-gpu")
                opcoes.add_argument("--log-level=3")
                opcoes.add_argument("--no-first-run")
                opcoes.add_argument("--no-default-browser-check")
                opcoes.add_argument("about:blank")

                driver = webdriver.Chrome(options=opcoes)

            # === MICROSOFT EDGE ===
            elif navegador == 'edge':
                opcoes = webdriver.EdgeOptions()
                if not mostrar_tela_navegador:
                    opcoes.add_argument("--headless")
                opcoes.add_argument("--disable-gpu")
                opcoes.add_argument("--log-level=3")
                path_edge = EdgeChromiumDriverManager().install()
                try:
                    from selenium.webdriver.edge.service import Service as EdgeService
                    service_obj = EdgeService(path_edge)
                    driver = webdriver.Edge(service=service_obj, options=opcoes)
                except Exception:
                    try:
                        driver = webdriver.Edge(executable_path=path_edge, options=opcoes)
                    except Exception as inner:
                        logging.warning(f"Fallback Edge falhou: {inner}")
                        raise

            # === MOZILLA FIREFOX ===
            elif navegador == 'firefox':
                opcoes = webdriver.FirefoxOptions()
                if not mostrar_tela_navegador:
                    opcoes.add_argument("-headless")
                opcoes.add_argument("--log-level=3")
                gecko_path = GeckoDriverManager().install()
                try:
                    from selenium.webdriver.firefox.service import Service as FirefoxService
                    service_obj = FirefoxService(gecko_path)
                    driver = webdriver.Firefox(service=service_obj, options=opcoes)
                except Exception:
                    try:
                        driver = webdriver.Firefox(executable_path=gecko_path, options=opcoes)
                    except Exception as inner:
                        logging.warning(f"Fallback Firefox falhou: {inner}")
                        raise

            else:
                logging.warning(f"Preferência de navegador desconhecida: {navegador} — pulando.")
                continue

            if driver:
                logging.info(f"{navegador.capitalize()} iniciado com sucesso.")
                try:
                    driver.get("https://www.google.com/maps")
                    driver.maximize_window()  # garante que o navegador abra em tela cheia
                    logging.info("Google Maps aberto com sucesso e janela maximizada.")
                except Exception as e:
                    logging.warning(f"Falha ao abrir o Google Maps automaticamente: {e}")
                return driver

        except Exception as erro:
            logging.warning(f"Falha ao iniciar {navegador}: {erro}. Tentando próximo navegador.")
            # continua para o próximo navegador da lista

    logging.critical("Não foi possível iniciar nenhum navegador. Verifique os drivers e dependências.")
    raise SeleniumError("Erro abrir o navegador.")


def abrir_navegador():
    """
    Tenta abrir o navegador várias vezes até atingir o número máximo de tentativas.

    Essa função executa múltiplas tentativas de inicializar o driver Selenium,
    registrando logs detalhados sobre cada tentativa. Se todas as tentativas falharem,
    uma exceção `SeleniumError` é lançada para interromper o fluxo de execução.

    Returns:
        WebDriver: Instância do navegador iniciada com sucesso.

    Raises:
        SeleniumError: Se todas as tentativas de abrir o navegador falharem.

    Notes:
        - O número máximo de tentativas é definido pela variável global `tentativas_maximas`.
        - Entre as tentativas, há um intervalo de 5 segundos.
        - Logs são registrados nos níveis DEBUG, WARNING e CRITICAL.
    """
    for tentativa in range(1, tentativas_maximas + 1):
        logging.debug(f"Tentativa {tentativa} de {tentativas_maximas} para abrir o navegador...")

        driver = criar_driver()

        if driver:
            logging.debug(f"Navegador iniciado com sucesso na tentativa {tentativa}.")
            return driver
        else:
            logging.warning(f"Tentativa {tentativa} falhou ao abrir o navegador.")
            if tentativa < tentativas_maximas:
                logging.debug("Aguardando 5 segundos antes da próxima tentativa...")
                sleep(5)


    logging.critical("Todas as tentativas de abrir o navegador falharam. Interrompendo a execução.")
    raise SeleniumError("Erro abrir o navegador.")

def navegar_para_url(driver, url):
    """
    Navega até a URL especificada e aguarda o carregamento completo da página.

    Esta função utiliza o Selenium WebDriver para abrir uma página web e aguarda
    até que o documento esteja totalmente carregado (estado 'complete'), indicando
    que o DOM foi renderizado e o carregamento inicial da página foi concluído.

    Args:
        driver (WebDriver): Instância ativa do Selenium WebDriver.
        url (str): Endereço da página a ser acessada.

    Raises:
        SeleniumError: Caso o carregamento da página exceda o tempo limite
            ou ocorra qualquer outro erro durante a navegação.

    Notes:
        - Essa função não garante que elementos dinâmicos (carregados via JavaScript)
          estejam disponíveis; apenas que o DOM principal foi carregado.
        - Para páginas com carregamento assíncrono (ex: Google Maps),
          é recomendável combinar esta função com uma espera por elemento específico.
    """
    try:
        logging.debug(f"Iniciando navegação para URL: {url}")
        driver.get(url)
        logging.debug("Comando driver.get() executado, aguardando carregamento da página.")

        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        logging.debug(f"Página carregada com sucesso: {url}")

    except TimeoutException:
        logging.error(f"O carregamento da página excedeu o tempo limite de {15}s: {url}")
        raise SeleniumError(f"Timeout ao carregar a página: {url}")

    except Exception as ex:
        logging.error(f"Erro inesperado ao navegar para '{url}': {ex}")
        raise SeleniumError(f"Erro ao acessar '{url}': {ex}")

def fechar_navegador(driver):
    """
    Fecha o navegador controlado pelo Selenium WebDriver de forma segura e controlada.

    Essa função tenta encerrar a sessão do WebDriver com logs detalhados do processo.
    Caso ocorra uma falha (por exemplo, o driver já ter sido finalizado ou a instância
    estar corrompida), o erro é capturado e registrado no log.

    Args:
        driver (WebDriver): Instância ativa do Selenium WebDriver a ser encerrada.
    """
    logging.debug("Iniciando processo de encerramento do navegador...")

    try:
        driver.quit()
        logging.info("Navegador encerrado com sucesso.")
        logging.debug("Driver encerrado e recursos liberados corretamente.")

    except Exception as e:
        logging.error(f"Falha ao encerrar o navegador: {e}")