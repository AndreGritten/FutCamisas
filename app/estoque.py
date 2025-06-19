from produtos import *
def adicionar_quantidade_produto():
    while True:
        listar_produtos()
        try:
            id_produto = input("Informe o ID do produto para adicionar quantidade (ou Enter para sair): ").strip()
            if id_produto == "":
                break  # Sai da função se o usuário apertar Enter sem digitar
            id_produto = int(id_produto)
        except ValueError:
            print("ID inválido.")
            continue

        sql_buscar = "SELECT tamanhos FROM produtos WHERE id = ?"
        resultado = consultar(sql_buscar, (id_produto,))

        if not resultado:
            print(f"Produto com ID {id_produto} não encontrado.")
            continue

        tamanhos_list = json.loads(resultado[0][0])

        while True:
            tamanho = input("Informe o tamanho que deseja adicionar (ex.: P, M, G) (ou Enter para mudar de produto): ").upper().strip()
            if tamanho == "":
                break  # Sai para escolher outro produto

            if tamanho not in tamanhos_list:
                print(f"O tamanho {tamanho} não está cadastrado para este produto.")
                continue

            try:
                quantidade_adicional = int(input(f"Quantidade que deseja adicionar no tamanho {tamanho}: "))
            except ValueError:
                print("Quantidade inválida.")
                continue

            resultado_estoque = consultar(
                "SELECT quantidade FROM estoque WHERE produto_id = ? AND tamanho = ?",
                (id_produto, tamanho)
            )

            if resultado_estoque:
                nova_quantidade = resultado_estoque[0][0] + quantidade_adicional
                executar_comando(
                    "UPDATE estoque SET quantidade = ? WHERE produto_id = ? AND tamanho = ?",
                    (nova_quantidade, id_produto, tamanho)
                )
            else:
                executar_comando(
                    "INSERT INTO estoque (produto_id, tamanho, quantidade) VALUES (?, ?, ?)",
                    (id_produto, tamanho, quantidade_adicional)
                )

            print(f"Quantidade adicionada com sucesso no produto ID {id_produto}, tamanho {tamanho}.")

        # Depois de sair do loop de tamanhos, pergunta se quer continuar com outro produto
        continuar_produto = input("Deseja adicionar quantidade em outro produto? (S/N): ").strip().upper()
        if continuar_produto != "S":
            break


def check_product_in_stock():
    listar_produtos()
