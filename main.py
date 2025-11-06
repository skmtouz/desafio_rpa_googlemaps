from app.logs import configurar_logs
from app.constantes import arquivo_log
from domain.use_case import buscar_informacoes
import logging


def main():
    configurar_logs(arquivo_log)
    logging.info("Automação iniciada.")

    tipo = "academias"
    buscar_informacoes(tipo)

    tipo = "sorveterias"
    buscar_informacoes(tipo)
    
    tipo = "restaurantes"
    buscar_informacoes(tipo)

    logging.info("Automação finalizada.")


if __name__ == "__main__":
    main()
