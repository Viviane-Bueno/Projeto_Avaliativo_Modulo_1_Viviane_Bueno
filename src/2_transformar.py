import unicodedata
import pandas as pd
from sqlalchemy import create_engine, text
from config import POSTGRES_CONFIG

# Cria a engine de conexão com o PostgreSQL
url_conexao = f"postgresql+psycopg2://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['dbname']}"
engine = create_engine(url_conexao)

def limpar_nome_colunas(df):
    """Padroniza os nomes das colunas para snake_case (sem acentos, espaços ou carateres especiais)."""
    novas_colunas = []
    for col in df.columns:
        nfkd = unicodedata.normalize('NFKD', col)
        col_sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
        
        col_limpa = (
            col_sem_acento.lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            .replace(".", "")
            .replace("/", "_")
            .replace("º", "")
            .replace("-", "_")
            .strip("_")
        )
        novas_colunas.append(col_limpa)
    
    df.columns = novas_colunas
    return df

def transformar_e_carregar_silver():
    print("Iniciando o processo de transformação para a camada Silver...")
    
    try:
        # 1. Lê os dados da camada Raw
        print("Lendo tabelas da camada Raw...")
        df_viagem = pd.read_sql("SELECT * FROM public.raw_viagem", engine)
        df_pagamento = pd.read_sql("SELECT * FROM public.raw_pagamento", engine)
        df_passagem = pd.read_sql("SELECT * FROM public.raw_passagem", engine)
        df_trecho = pd.read_sql("SELECT * FROM public.raw_trecho", engine)

        # 2. Padroniza os nomes das colunas
        print("Padronizando nomes das colunas para a camada Silver...")
        df_viagem = limpar_nome_colunas(df_viagem)
        df_pagamento = limpar_nome_colunas(df_pagamento)
        df_passagem = limpar_nome_colunas(df_passagem)
        df_trecho = limpar_nome_colunas(df_trecho)

        # 3. Remove as tabelas Silver antigas com CASCADE para evitar conflitos de chaves
        print("Removendo tabelas Silver antigas e recriando limpas...")
        with engine.begin() as conn:
            conn.execute(text("""
                DROP TABLE IF EXISTS public.silver_pagamento CASCADE;
                DROP TABLE IF EXISTS public.silver_passagem CASCADE;
                DROP TABLE IF EXISTS public.silver_trecho CASCADE;
                DROP TABLE IF EXISTS public.silver_viagem CASCADE;
            """))

        # 4. Grava e recria as tabelas automaticamente com base nos DataFrames limpos
        print("Gravando novas tabelas na camada Silver...")
        df_viagem.to_sql('silver_viagem', engine, schema='public', if_exists='replace', index=False)
        df_pagamento.to_sql('silver_pagamento', engine, schema='public', if_exists='replace', index=False)
        df_passagem.to_sql('silver_passagem', engine, schema='public', if_exists='replace', index=False)
        df_trecho.to_sql('silver_trecho', engine, schema='public', if_exists='replace', index=False)

        print("\n🎉 Processo de transformação e carga da camada Silver finalizado com sucesso!")

    except Exception as e:
        print(f"\n❌ Erro crítico durante a transformação para a Silver: {e}")
        raise

if __name__ == "__main__":
    transformar_e_carregar_silver()