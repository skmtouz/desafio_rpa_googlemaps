import logging

class ColorFormatter(logging.Formatter):
    """
    Formata mensagens de log com cores diferentes por nível,
    mantendo a mensagem em cor padrão (neutra).
    """

    COLORS = {
        "DEBUG": "\033[90m",     # cinza claro
        "INFO": "\033[36m",      # ciano
        "WARNING": "\033[33m",   # amarelo
        "ERROR": "\033[31m",     # vermelho
        "CRITICAL": "\033[41m",  # fundo vermelho
    }
    RESET = "\033[0m"
    MESSAGE_COLOR = "\033[97m"  # branco (texto principal)

    def format(self, record):
        # Salva o texto original do nível e da mensagem
        original_levelname = record.levelname
        original_msg = record.msg

        # Aplica cor apenas ao nível
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"

        # Mensagem volta ao branco (sem “vazar” a cor)
        record.msg = f"{self.MESSAGE_COLOR}{record.msg}{self.RESET}"

        formatted = super().format(record)

        # Restaura os valores originais (boa prática)
        record.levelname = original_levelname
        record.msg = original_msg
        return formatted

def configurar_logs(nome_do_arquivo_log: str):
    """
    Configura o sistema de logs para registrar mensagens em arquivo e no console com cores equilibradas.

    Args:
        nome_do_arquivo_log (str): Caminho do arquivo de log a ser utilizado.

    Esta função define:
        - Um manipulador de arquivo (FileHandler) para salvar logs (sem cores).
        - Um manipulador de console (StreamHandler) com cores por nível.
        - Nível mínimo DEBUG para capturar todos os eventos relevantes.
    """
    formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Arquivo (sem cor)
    file_handler = logging.FileHandler(nome_do_arquivo_log)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formato)

    # Console (com cores)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(ColorFormatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Reduz ruído do Selenium e urllib3
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

    logger.info("O sistema de logs foi iniciado com cores ajustadas no console.")