from banco import get_conexao


def carregar_gold():
    conn = get_conexao()
    cur = conn.cursor()
    print("Gold já criado pelas views - finalizando...")
    conn.commit()
    cur.close()
    conn.close()
    print("Load pronto!")


if __name__ == "__main__":
    carregar_gold()
