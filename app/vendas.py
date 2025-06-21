from bancoDeDados.conexao import *
from produtos import *

def calcular_total(carrinho):
    return sum(item["preco_unitario"] * item["quantidade"] for item in carrinho)

def realizar_venda():
    email = input("Digite seu email: ").strip()
    senha = input("Digite sua senha: ").strip()

    sql = "SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?"
    resultado = consultar(sql, (email, senha))

    if not resultado:
        print("Login inválido.")
        return

    usuario_id, nome = resultado[0]
    print(f"Bem-vindo, {nome}!")

    carrinho = []

    while True:
        listar_produtos()

        try:
            id_produto = int(input("ID do produto (ou 0 para finalizar): "))
            if id_produto == 0:
                break
        except ValueError:
            print("ID inválido.")
            continue

        sql_prod = "SELECT nome, preco, tamanhos FROM produtos WHERE id = ?"
        produto = consultar(sql_prod, (id_produto,))

        if not produto:
            print("Produto não encontrado.")
            continue

        nome_produto, preco, tamanhos_json = produto[0]
        tamanhos = json.loads(tamanhos_json)

        tamanho = input(f"Escolha o tamanho {tamanhos}: ").strip().upper()
        if tamanho not in tamanhos:
            print("Tamanho inválido.")
            continue

        try:
            quantidade = int(input("Quantidade desejada: "))
        except ValueError:
            print("Quantidade inválida.")
            continue

        # Verificar estoque
        sql_estoque = '''
            SELECT quantidade FROM estoque
            WHERE produto_id = ? AND tamanho = ?
        '''
        estoque = consultar(sql_estoque, (id_produto, tamanho))

        if not estoque or estoque[0][0] < quantidade:
            print("Estoque insuficiente.")
            continue

        carrinho.append({
            "produto_id": id_produto,
            "nome": nome_produto,
            "tamanho": tamanho,
            "quantidade": quantidade,
            "preco_unitario": preco
        })

        print(f"Adicionado {quantidade}x {nome_produto} (Tam: {tamanho}) ao carrinho.")

    if not carrinho:
        print("Carrinho vazio. Venda cancelada.")
        return

    print("\nResumo da compra:")
    for item in carrinho:
        print(f"- {item['nome']} | Tam: {item['tamanho']} | Qtde: {item['quantidade']} | Unitário: R$ {item['preco_unitario']}")

    total = calcular_total(carrinho)
    print(f"Total: R$ {total:.2f}")

    confirmar = input("Deseja finalizar a compra? (S/N): ").strip().upper()
    if confirmar == "S":
        finalizar_venda(usuario_id, carrinho)
    else:
        print("Venda cancelada.")


def finalizar_venda(usuario_id, carrinho):
    total = calcular_total(carrinho)

    sql_venda = '''
        INSERT INTO vendas (usuario_id, data, status, total)
        VALUES (?, datetime('now'), 'pago', ?)
    '''
    cursor, conexao = executar_comando_com_retorno(sql_venda, (usuario_id, total))
    venda_id = cursor.lastrowid

    for item in carrinho:
        sql_item = '''
            INSERT INTO itens_venda (venda_id, produto_id, tamanho, quantidade, preco_unitario)
            VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(sql_item, (
            venda_id,
            item["produto_id"],
            item["tamanho"],
            item["quantidade"],
            item["preco_unitario"]
        ))

        # Atualizar o estoque
        sql_update_estoque = '''
            UPDATE estoque
            SET quantidade = quantidade - ?
            WHERE produto_id = ? AND tamanho = ?
        '''
        cursor.execute(sql_update_estoque, (
            item["quantidade"],
            item["produto_id"],
            item["tamanho"]
        ))

    conexao.commit()
    conexao.close()
    print(f"Venda concluída com sucesso! ID da venda: {venda_id}")


def buscar_historico_vendas(usuario_id):
    sql_vendas = '''
        SELECT id, data, status, total FROM vendas
        WHERE usuario_id = ?
    '''
    vendas = consultar(sql_vendas, (usuario_id,))

    if not vendas:
        print("Nenhuma venda encontrada para este usuário.")
        return

    for venda in vendas:
        venda_id, data, status, total = venda
        print(f"\nVenda ID: {venda_id} | Data: {data} | Status: {status} | Total: R$ {total}")

        sql_itens = '''
            SELECT p.nome, iv.tamanho, iv.quantidade, iv.preco_unitario
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            WHERE iv.venda_id = ?
        '''
        itens = consultar(sql_itens, (venda_id,))

        for item in itens:
            nome, tamanho, quantidade, preco = item
            print(f"- {nome} | Tam: {tamanho} | Qtde: {quantidade} | Unitário: R$ {preco}")

        print('-'*40)


def listar_vendas():
    sql = '''
        SELECT v.id, v.data, v.status, v.total,
               u.nome, u.cpf, u.email
        FROM vendas v
        JOIN usuarios u ON v.usuario_id = u.id
        ORDER BY v.data DESC
    '''
    vendas = consultar(sql)

    if not vendas:
        print("\nNão há vendas registradas no sistema.")
        return

    print("\n===== LISTAGEM DE TODAS AS VENDAS =====")
    for venda in vendas:
        venda_id, data, status, total, nome, cpf, email = venda
        print(f"\nVenda ID: {venda_id}")
        print(f"Cliente: {nome} | CPF: {cpf} | Email: {email}")
        print(f"Data: {data}")
        print(f"Status: {status}")
        print(f"Total: R$ {total:.2f}")

        sql_itens = '''
            SELECT p.nome, iv.tamanho, iv.quantidade, iv.preco_unitario
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            WHERE iv.venda_id = ?
        '''
        itens = consultar(sql_itens, (venda_id,))

        if itens:
            print("Itens da venda:")
            for item in itens:
                nome_produto, tamanho, quantidade, preco_unitario = item
                print(f"  - {nome_produto} | Tam: {tamanho} | Qtde: {quantidade} | Unitário: R$ {preco_unitario:.2f}")
        else:
            print("Nenhum item encontrado para esta venda.")

        print('-'*50)
