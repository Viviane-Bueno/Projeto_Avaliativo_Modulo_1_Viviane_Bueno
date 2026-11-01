"""
banco.py
--------
Gerencia a conexão e operações com o PostgreSQL de forma totalmente flexível e segura.
"""

import psycopg2
from psycopg2 import Error
from psycopg2.extras import execute_values
from config import POSTGRES_CONFIG

def conectar():
    """Abre uma conexão com o PostgreSQL usando as configurações do config.py."""
    try:
        return psycopg2.connect(**POSTGRES_CONFIG)
    except Error as erro:
        raise RuntimeError(
            f"Não foi possível conectar ao PostgreSQL: {erro}"
        )

def executar_query(conexao_ou_sql, sql=None, parametros=None, **kwargs):
    """Executa um comando SQL aceitando múltiplos formatos de chamada."""
    if sql is None:
        sql = conexao_ou_sql
        conexao = conectar()
        fechar_conexao = True
    else:
        conexao = conexao_ou_sql
        fechar_conexao = False

    cursor = conexao.cursor()
    try:
        cursor.execute(sql, parametros or ())
        conexao.commit()
    except Exception as e:
        conexao.rollback()
        raise e
    finally:
        cursor.close()
        if fechar_conexao:
            conexao.close()

def carregar_dataframe_em_lote(*args, **kwargs):
    """
    Insere dados em lote aceitando qualquer variação de argumentos 
    e lidando com DataFrames do Pandas de forma segura.
    """
    conexao = kwargs.get("conexao")
    sql_insert = kwargs.get("sql_insert") or kwargs.get("sql")
    linhas = kwargs.get("linhas") or kwargs.get("Linhas") or kwargs.get("dados")

    if not conexao and len(args) > 0:
        conexao = args[0]
    if not sql_insert and len(args) > 1:
        sql_insert = args[1]
    if not linhas and len(args) > 2:
        linhas = args[2]

    # Validação segura para evitar o erro do DataFrame
    if linhas is None:
        return
    
    import pandas as pd
    if isinstance(linhas, pd.DataFrame):
        if linhas.empty:
            return
        linhas = [tuple(x) for x in linhas.to_numpy()]
    else:
        if hasattr(linhas, "__len__") and len(linhas) == 0:
            return

    fechar_conexao = False
    if not conexao:
        conexao = conectar()
        fechar_conexao = True

    cursor = conexao.cursor()
    try:
        execute_values(cursor, sql_insert, linhas)
        conexao.commit()
    except Exception as e:
        conexao.rollback()
        raise e
    finally:
        cursor.close()
        if fechar_conexao:
            conexao.close()