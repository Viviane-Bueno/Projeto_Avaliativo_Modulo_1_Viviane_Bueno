import os
from pathlib import Path

# Caminhos do projeto
PASTA_RAIZ = Path(__file__).resolve().parent.parent
PASTA_DADOS = PASTA_RAIZ / "data"
DATA_RAW_DIR = PASTA_DADOS / "raw"

# Leitura simples do arquivo .env
def carregar_env():
    arquivo_env = PASTA_RAIZ / ".env"
    if not arquivo_env.exists():
        return
    for linha in arquivo_env.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave.strip(), valor.strip())

carregar_env()

# Credenciais do PostgreSQL alinhadas com o seu .env e pgAdmin
POSTGRES_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", "1234")),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASSWORD", "123456"),
    "dbname": os.environ.get("DB_NAME", "Projeto_Avaliativo_Modulo_1_Viviane_Bueno"),
}

ANO = "2025"
DRIVE_FILE_ID = os.environ.get("DRIVE_FILE_ID", "1b9Yc_s9gm6TAERY3BjOw2bixu70X3tZL")
TAMANHO_BLOCO = 50000

ARQUIVOS = {
    "viagem": {"csv": f"{ANO}_Viagem.csv", "tabela_raw": "raw_viagem"},
    "pagamento": {"csv": f"{ANO}_Pagamento.csv", "tabela_raw": "raw_pagamento"},
    "passagem": {"csv": f"{ANO}_Passagem.csv", "tabela_raw": "raw_passagem"},
    "trecho": {"csv": f"{ANO}_Trecho.csv", "tabela_raw": "raw_trecho"},
}

CSV_SEPARADOR = ";"
CSV_ENCODING = "latin-1"