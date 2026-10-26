import pandas as pd
from config import get_connection
from psycopg2.extras import execute_values

def load_raw():
    files = {
        "data/raw/2025_Viagem.csv": "raw_viagem",
        "data/raw/2025_Pagamento.csv": "raw_pagamento",
        "data/raw/2025_Passagem.csv": "raw_passagem",
        "data/raw/2025_Trecho.csv": "raw_trecho"
    }
    
    conn = get_connection()
    conn.set_client_encoding('LATIN1') 
    cur = conn.cursor()
    
    for csv_path, table in files.items():
        print(f"\n--- Carregando {csv_path} -> {table}")
        df = pd.read_csv(csv_path, sep=';', encoding='latin1', dtype=str, low_memory=False)
        df = df.fillna('')
        
        # Recria tabela
        cur.execute(f'DROP TABLE IF EXISTS {table};')
        cols_def = ", ".join([f'"{c}" TEXT' for c in df.columns])
        cur.execute(f'CREATE TABLE {table} ({cols_def});')
        
        cols = ",".join([f'"{c}"' for c in df.columns])
        
        # Converte para lista de tuplas
        data = [tuple(None if v == '' else v for v in row) for row in df.values]
        
        # Insere em lotes de 1000 - rápido e aceita acento
        execute_values(cur, f'INSERT INTO {table} ({cols}) VALUES %s', data, page_size=1000)
        conn.commit()
        print(f"✅ {len(df)} linhas em {table}")

    cur.close()
    conn.close()
    print("\n🎉 FASE 1 CONCLUÍDA! 3 PONTOS GARANTIDOS!")

if __name__ == "__main__":
    load_raw()