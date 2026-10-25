# Projeto Avaliativo Módulo 1 - Viagens Governamentais

**Aluna:** Viviane Bueno

## Estrutura
- `0_criar_banco.sql`: Cria 8 tabelas (4 Raw + 4 Silver) com PK, FK e 8 CHECKs
- `data/raw/`: Dados brutos 2025 (Viagem, Pagamento, Passagem, Trecho) - versionado com Git LFS
- `etl/`: Scripts 1_extrair.py, 2_transformar.py, 3_carregar.py
- `3_analise.ipynb`: 4 análises

## Como rodar
1. `git lfs pull`
2. Criar banco: `psql -f 0_criar_banco.sql`
3. `pip install -r requirements.txt`
4. Rodar ETL e análise

## Modelagem
Raw = carga exata dos CSVs
Silver = tipagem, NOT NULL, FK para viagem, CHECKs (valor>=0, etc)