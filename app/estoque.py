import json
from .produtos import listar_produtos
from .bancoDeDados.conexao import executar_comando, consultar

def adicionar_quantidade_produto():
    while True:
        listar_produtos()
        try:
            id_produto_input = input("Informe o ID do produto para adicionar quantidade (ou Enter para sair): ").strip()
            if id_produto_input == "":
                break
            id_produto = int(id_produto_input)
        except ValueError:
            print("ID inválido. Digite um número válido.")
            continue

        sql_buscar_tamanhos = "SELECT tamanhos FROM produtos WHERE id = ?"
        resultado_tamanhos = consultar(sql_buscar_tamanhos, (id_produto,))

        if not resultado_tamanhos:
            print(f"Produto com ID {id_produto} não encontrado.")
            continue

        tamanhos_disponiveis = json.loads(resultado_tamanhos[0][0])
        print(f"Tamanhos disponíveis para este produto: {', '.join(tamanhos_disponiveis)}")

        while True:
            tamanho = input("Informe o tamanho que deseja adicionar (ex.: P, M, G) (ou Enter para voltar para escolha de produto): ").upper().strip()
            if tamanho == "":
                break

            if tamanho not in tamanhos_disponiveis:
                print(f"O tamanho '{tamanho}' não está cadastrado para este produto. Por favor, escolha um dos disponíveis.")
                continue

            try:
                quantidade_adicional = int(input(f"Quantidade que deseja adicionar no tamanho {tamanho}: "))
                if quantidade_adicional <= 0:
                    print("Quantidade deve ser um número positivo.")
                    continue
            except ValueError:
                print("Quantidade inválida. Informe um número inteiro.")
                continue

            sql_buscar_estoque = "SELECT quantidade FROM estoque WHERE produto_id = ? AND tamanho = ?"
            resultado_estoque = consultar(sql_buscar_estoque, (id_produto, tamanho))

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

            continuar_tamanho = input("Adicionar mais quantidade a outro tamanho deste produto? (S/N): ").strip().upper()
            if continuar_tamanho != "S":
                break

        continuar_produto = input("Deseja adicionar quantidade em outro produto? (S/N): ").strip().upper()
        if continuar_produto != "S":
            break


def check_product_in_stock():
    listar_produtos()