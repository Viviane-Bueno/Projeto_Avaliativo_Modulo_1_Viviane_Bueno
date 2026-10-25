import psycopg2
from config import DB_CONFIG


def extrair_dados():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT * FROM raw_viagem LIMIT 5;")
    dados = cur.fetchall()
    cur.close()
    conn.close()
    return dados
