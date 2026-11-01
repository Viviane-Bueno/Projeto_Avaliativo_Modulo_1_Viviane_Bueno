import os
import pandas as pd
from sqlalchemy import create_engine
from config import POSTGRES_CONFIG
from banco import executar_query

# Cria a engine de conexão diretamente com as configurações do projeto
url_conexao = f"postgresql+psycopg2://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['dbname']}"
engine = create_engine(url_conexao)

def carregar_csv_para_raw(nome_csv: str, nome_tabela: str):
    """Lê um CSV local em blocos e carrega na tabela Raw correspondente no PostgreSQL."""
    caminho_csv = os.path.join("data", "raw", nome_csv)
    
    if not os.path.exists(caminho_csv):
        print(f"⚠️ Aviso: O ficheiro {nome_csv} não foi encontrado em {caminho_csv}.")
        return

    print(f"Processando e carregando {nome_csv} na tabela {nome_tabela}...")
    
    try:
        chunksize = 50000
        primeiro_lote = True
        
        tabela_limpa = nome_tabela.replace('public.', '')

        for chunk in pd.read_csv(caminho_csv, sep=';', encoding='latin-1', dtype=str, chunksize=chunksize, low_memory=False):
            chunk = chunk.where(pd.notnull(chunk), None)
            
            if chunk.empty:
                continue
                
            if primeiro_lote:
                chunk.to_sql(tabela_limpa, engine, schema='public', if_exists='replace', index=False)
                primeiro_lote = False
            else:
                chunk.to_sql(tabela_limpa, engine, schema='public', if_exists='append', index=False)
                
        print(f"✅ Tabela {nome_tabela} carregada com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao carregar a tabela {nome_tabela}: {e}")
        raise

if __name__ == "__main__":
    try:
        arquivos_tabelas = {
            "2025_Viagem.csv": "public.raw_viagem",
            "2025_Pagamento.csv": "public.raw_pagamento",
            "2025_Passagem.csv": "public.raw_passagem",
            "2025_Trecho.csv": "public.raw_trecho"
        }

        for nome_csv, nome_tabela in arquivos_tabelas.items():
            carregar_csv_para_raw(nome_csv, nome_tabela)

        print("\n🎉 Processo de extração da camada Raw finalizado com sucesso!")

    except Exception as e:
        print(f"\n❌ Erro crítico na extração: {e}")