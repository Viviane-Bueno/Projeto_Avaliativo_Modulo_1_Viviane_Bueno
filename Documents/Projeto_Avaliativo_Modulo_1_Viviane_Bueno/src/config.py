import os
import psycopg2
from dotenv import load_dotenv

# Carrega o .env que está na raiz do projeto
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "Projeto_Avaliativo_Modulo_1_Viviane_Bueno")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

def get_connection():
    """Cria conexão com PostgreSQL"""
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def test_connection():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print("✅ Conectado no PostgreSQL:", cur.fetchone()[0])
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("❌ Erro de conexão:", e)
        return False

if __name__ == "__main__":
    test_connection()