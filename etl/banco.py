import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="Projeto_Avaliativo_Modulo_1_Viviane_Bueno",
        user="postgres",
        password="123456",  # ← coloca sua senha real aqui
        port=1234,
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM raw_viagem LIMIT 5;")
    dados = cur.fetchall()

    print("✅ Conectou! Resultados:")
    for linha in dados:
        print(linha)

    cur.close()
    conn.close()
    print("✅ Pronto!")

except Exception as e:
    print(f"❌ Erro: {e}")
