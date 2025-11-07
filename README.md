# Desafio Técnico — Automacao RPA Google Maps

## 📌 Descrição

Este projeto automatiza a coleta de informações de estabelecimentos no **Google Maps** (ex: academias, restaurantes e sorveterias).\
A automação extrai dados como **nome**, **tipo**, **nota**, **quantidade de avaliações** e **endereço**, salvando-os em **JSON** e **Excel**.

---

## ⚙️ Instruções de instalação e execução

### 1️⃣ Requisitos mínimos

- **Python 3.10+**
- **Google Chrome** (instalado localmente)
- Conexão com a internet

---

### 2️⃣ Instalação

**1. Clonar o repositório**

```bash
git clone https://github.com/skmtouz/desafio_rpa_googlemaps.git
cd desafio_rpa_googlemaps
```

**2. Criar e ativar o ambiente virtual**

```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# (ou em bash: source venv/bin/activate)
```

**3. Instalar dependências**

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Execução

Com o ambiente ativo, execute:

```bash
python main.py
```

Durante a execução, o robô:

1. Abre o Google Maps via Selenium.
2. Pesquisa os tipos de estabelecimentos definidos em `app/constantes.py`.
3. Extrai os dados fornecidos pelo Google Maps.
4. Gera dois arquivos por tipo:
   - `NOME_DO_ESTABELECIMENTO.json`
   - `NOME_DO_ESTABELECIMENTO.xlsx`

---

## ⚙️ Dependências necessárias

As principais bibliotecas utilizadas são:

| Biblioteca            | Função principal                                    |
| --------------------- | --------------------------------------------------- |
| **selenium**          | Controle do navegador e interação com o Google Maps |
| **webdriver-manager** | Gerencia automaticamente o driver do navegador      |
| **pandas**            | Estruturaçao e manipulação de dados                 |
| **openpyxl**          | Geracao e formatação da planilha Excel              |
| **logging**           | Registro das operações em log                       |

Instalação manual (caso necessário):

```bash
pip install selenium webdriver-manager pandas openpyxl
```

---

## 🖥️ Dados que precisam ser alterados ao executar em outro computador

Todas as variáveis configuraveis estão centralizadas em:

```
app/constantes.py
```

### Principais variaveis que podem ser ajustadas:

| Variável                                         | Descrição                                                          |
| ------------------------------------------------ | ------------------------------------------------------------------ |
| `mostrar_tela_navegador`                         | Exibe ou oculta o navegador durante a execução (`True` / `False`). |
| `quantidade_de_resultados`                     | Número máximo de estabelecimentos coletados por categoria.         |
| `caminho_arquivos` | Caminhos onde os arquivos serão salvos.                            |
| `estabelecimentos`                                | Lista de categorias a serem pesquisadas no Google Maps.            |

> 💡 Caso o projeto seja movido para outro computador, apenas revise os **caminhos dos arquivos** e **os navegadores instalados**.

---

## 📁 Arquitetura de organização de pastas

```
desafio_rpa_googlemaps/
├─ app/                       # Pacote reservado para configurações da aplicação
│  ├─ constantes.py
│  ├─ exceptions.py
│  ├─ logs.py
│  └─ utils.py
├─ arquivos_gerados/          # Pasta reservada para disponibilização de arquivos
├─ domain/                    # Pacote reservado para todos os casos de usos necessários da aplicação
│  └─ use_case.py
├─ infra/                     # Pacote reservada do para todas as comunicações com a infraestrutura da aplicação
│  └─ file_provider.py
├─ main.py
└─ README.md
```

---

## 📝 Logs

- Todos os logs de execução sao salvos em `automação.log` na pasta `arquivos_gerados`

---

## ✅ Observações

- O código segue boas praticas de **Clean Code** e separação por camadas (`app`, `domain`, `infra`).
- Caso algum XPath seja alterado no Google Maps, ajuste os caminhos em `app/constantes.py`.
- O script foi testado em ambiente Windows com Python 3.13.3 e Google Chrome atualizado.
- Todos os metódos utilizados no projeto estão documentados e com logs.
- Para fins de teste, defina `quantidade_maxima_por_tipo = 3` em `constantes.py` — assim o robô coleta poucos registros e roda mais rápido.

---


