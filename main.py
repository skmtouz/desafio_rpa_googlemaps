from app.logs import configurar_logs
from app.constantes import estabelecimentos
from domain.use_case import buscar_informacoes
import logging


def main():
    configurar_logs()
    logging.info("Automação iniciada.")
    for tipo in estabelecimentos:
        buscar_informacoes(tipo)

    logging.info("Automação finalizada.")


if __name__ == "__main__":
    main()
