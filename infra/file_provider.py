import json
import logging
import os

from app.constantes import arquivo_json
from app.exceptions import ArquivoError

def gerar_arquivo_json(nome_arquivo: str, json_conteudo: list):
    """
    Gera e salva um arquivo JSON formatado em um diretório específico,
    com logs detalhados de cada etapa do processo.

    Args:
        nome_arquivo (str): Nome base do arquivo (sem extensão).
        json_conteudo (list): Dados a serem salvos no arquivo.

    Raises:
        ArquivoError: Caso ocorra erro ao gerar o arquivo.
    """
    nome_arquivo_completo = f"{nome_arquivo}.json"
    caminho_arquivo = os.path.join(os.path.dirname(arquivo_json), nome_arquivo_completo)

    logging.debug(f"Iniciando geração do arquivo JSON: {nome_arquivo_completo}")
    logging.debug(f"Caminho completo: {caminho_arquivo}")

    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(json_conteudo, arquivo, ensure_ascii=False, indent=4)

        logging.info(
            f"Arquivo '{nome_arquivo_completo}' salvo com sucesso em '{os.path.dirname(arquivo_json)}' "
            f"({len(json_conteudo)} registros)."
        )
    except Exception as e:
        logging.critical(
            f"Falha ao gerar o arquivo '{nome_arquivo_completo}': {e}"
        )
        raise ArquivoError(f"Erro ao gerar o arquivo JSON '{nome_arquivo_completo}'.") from e