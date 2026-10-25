import psycopg2
import sys

sys.path.append("etl")
from config import DB_CONFIG


def transformar_dados():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    print("Limpando silver...")
    cur.execute(
        "TRUNCATE TABLE silver_trecho, silver_viagem, silver_passagem, silver_pagamento CASCADE;"
    )

    print("Copiando viagem...")
    cur.execute(
        "INSERT INTO silver_viagem (id_viagem) SELECT DISTINCT id_viagem FROM raw_viagem WHERE id_viagem IS NOT NULL;"
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Transform pronto!")


if __name__ == "__main__":
    transformar_dados()
