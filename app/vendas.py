import json
from datetime import datetime
from bancoDeDados.conexao import *
from produtos import *
from relatorios import * # Importa a nova função de relatório


def calcular_total(carrinho):
    return sum(item["preco_unitario"] * item["quantidade"] for item in carrinho)

def obter_produto_por_id_e_tamanho(id_produto, tamanho, conexao=None): # Adicionar conexao como parametro
    sql = "SELECT p.nome, p.preco, e.quantidade FROM produtos p JOIN estoque e ON p.id = e.produto_id WHERE p.id = ? AND e.tamanho = ?"
    resultado = consultar(sql, (id_produto, tamanho), conexao) # Passar a conexao
    if resultado:
        nome_produto, preco_produto, quantidade_estoque = resultado[0]
        return nome_produto, preco_produto, quantidade_estoque
    return None

def verificar_estoque(produto_id, tamanho, quantidade_desejada, conexao=None): # Adicionar conexao como parametro
    sql = "SELECT quantidade FROM estoque WHERE produto_id = ? AND tamanho = ?"
    resultado = consultar(sql, (produto_id, tamanho), conexao) # Passar a conexao
    if resultado and resultado[0][0] >= quantidade_desejada:
        return True
    return False

def salvar_venda(usuario_id, carrinho):
    total = calcular_total(carrinho)
    data_hora_venda = datetime.now()

    sql_venda = '''
        INSERT INTO vendas (usuario_id, data, status, total)
        VALUES (?, ?, 'pendente', ?)
    '''
    # 1. First, establish the main connection for this transaction
    cursor, conexao = executar_comando_com_retorno(sql_venda, (usuario_id, data_hora_venda.isoformat(), total))
    venda_id = cursor.lastrowid

    if not venda_id:
        conexao.rollback()
        conexao.close()
        return None

    # 2. Now that 'conexao' is defined, you can use it
    # Obter nome do cliente para o relatório
    sql_cliente_nome = "SELECT nome FROM usuarios WHERE id = ?"
    resultado_cliente = consultar(sql_cliente_nome, (usuario_id,), conexao) # Passa a conexão
    cliente_nome = resultado_cliente[0][0] if resultado_cliente else "Desconhecido"
    
    produtos_para_relatorio = []
    try:
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
            
            # Adiciona item formatado para o relatório
            produtos_para_relatorio.append({
                "nome": item["name"], 
                "tamanho": item["tamanho"],
                "quantidade": item["quantidade"],
                "preco_unitario": item["preco_unitario"]
            })

            sql_update_estoque = '''
                UPDATE estoque SET quantidade = quantidade - ?
                WHERE produto_id = ? AND tamanho = ?
            '''
            cursor.execute(sql_update_estoque, (
                item["quantidade"],
                item["produto_id"],
                item["tamanho"]
            ))
        conexao.commit()

        # Registrar no arquivo de relatórios APÓS o commit no banco de dados
        registrar_venda_em_arquivo(venda_id, cliente_nome, data_hora_venda.isoformat(), produtos_para_relatorio, total)
        return venda_id
    except sqlite3.Error as e:
        conexao.rollback()
        print(f"Erro ao salvar venda ou itens: {e}")
        return None
    finally:
        conexao.close()

def buscar_vendas_usuario(usuario_id):
    sql_vendas = '''
        SELECT id, data, status, total FROM vendas WHERE usuario_id = ? ORDER BY data DESC
    '''
    return consultar(sql_vendas, (usuario_id,))

def buscar_itens_venda(venda_id):
    sql_itens = '''
        SELECT p.nome, iv.tamanho, iv.quantidade, iv.preco_unitario
        FROM itens_venda iv
        JOIN produtos p ON iv.produto_id = p.id
        WHERE iv.venda_id = ?
    '''
    return consultar(sql_itens, (venda_id,))

def listar_todas_vendas():
    sql = '''
        SELECT v.id, v.data, v.status, v.total,
               u.nome, u.cpf, u.email
        FROM vendas v
        JOIN usuarios u ON v.usuario_id = u.id
        ORDER BY v.data DESC
    '''
    return consultar(sql)

def realizar_venda_interativo(usuario):
    usuario_id, nome, tipo_usuario, email, cpf = usuario
    print(f"\nBem-vindo(a) ao processo de compra, {nome}!")

    carrinho = []

    while True:
        listar_produtos()
        try:
            id_produto_input = input("ID do produto a adicionar (ou 0 para finalizar): ").strip()
            if id_produto_input == "0":
                break
            id_produto = int(id_produto_input)
        except ValueError:
            print("ID inválido. Digite um número válido ou 0 para finalizar.")
            continue

        sql_tamanhos_produto = "SELECT tamanhos FROM produtos WHERE id = ?"
        produto_info = consultar(sql_tamanhos_produto, (id_produto,))
        if not produto_info:
            print("Produto não encontrado.")
            continue

        tamanhos_disponiveis_list = json.loads(produto_info[0][0])

        if not tamanhos_disponiveis_list:
            print("Este produto não possui tamanhos disponíveis.")
            continue

        print(f"Tamanhos disponíveis para o produto: {', '.join(tamanhos_disponiveis_list)}")
        tamanho = input("Escolha o tamanho: ").strip().upper()

        if tamanho not in tamanhos_disponiveis_list:
            print("Tamanho inválido para este produto.")
            continue

        try:
            quantidade = int(input("Quantidade desejada: "))
            if quantidade <= 0:
                print("Quantidade deve ser positiva.")
                continue
        except ValueError:
            print("Quantidade inválida.")
            continue

        nome_produto, preco_unitario, estoque_atual = obter_produto_por_id_e_tamanho(id_produto, tamanho)
        if not nome_produto:
            print("Produto ou tamanho não encontrado no estoque.")
            continue


        if not verificar_estoque(id_produto, tamanho, quantidade):
            print(f"Estoque insuficiente para o tamanho {tamanho}. Disponível: {estoque_atual} un.")
            continue

        carrinho.append({
            "produto_id": id_produto,
            "nome": nome_produto,
            "tamanho": tamanho,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario
        })

        print(f"Adicionado {quantidade}x {nome_produto} (Tam: {tamanho}) ao carrinho.")

    if not carrinho:
        print("Carrinho vazio. Venda cancelada.")
        return

    print("\n--- Resumo da Compra ---")
    for item in carrinho:
        print(f"- {item['nome']} | Tam: {item['tamanho']} | Qtde: {item['quantidade']} | Unitário: R$ {item['preco_unitario']:.2f}")

    total_final = calcular_total(carrinho)
    print(f"Total: R$ {total_final:.2f}")

    confirmar = input("Deseja finalizar a compra? (S/N): ").strip().upper()
    if confirmar == "S":
        venda_id = salvar_venda(usuario_id, carrinho) # Agora salvar_venda lida com o nome do cliente
        if venda_id:
            print(f"Venda concluída com sucesso! ID da venda: {venda_id}")
        else:
            print("Falha ao finalizar a venda.")
    else:
        print("Venda cancelada.")


def buscar_historico_vendas_interativo(usuario_id):
    vendas = buscar_vendas_usuario(usuario_id)
    if not vendas:
        print("Nenhuma venda encontrada para este usuário.")
        return

    print(f"\n===== Histórico de Vendas (ID Usuário: {usuario_id}) =====")
    for venda in vendas:
        venda_id, data, status, total = venda
        print(f"\nVenda ID: {venda_id} | Data: {data} | Status: {status} | Total: R$ {total:.2f}")

        itens = buscar_itens_venda(venda_id)
        if itens:
            print("  Itens da venda:")
            for nome, tamanho, quantidade, preco in itens:
                print(f"    - {nome} | Tam: {tamanho} | Qtde: {quantidade} | Unitário: R$ {preco:.2f}")
        else:
            print("  Nenhum item encontrado para esta venda.")

        print('-'*50)

def listar_vendas_interativo():
    vendas = listar_todas_vendas()
    if not vendas:
        print("\nNão há vendas registradas no sistema.")
        return

    print("\n===== LISTAGEM DE TODAS AS VENDAS =====")
    for venda in vendas:
        venda_id, data, status, total, nome_usuario, cpf_usuario, email_usuario = venda
        print(f"\nVenda ID: {venda_id}")
        print(f"Cliente: {nome_usuario} (CPF: {cpf_usuario}) | Email: {email_usuario}")
        print(f"Data: {data}")
        print(f"Status: {status}")
        print(f"Total: R$ {total:.2f}")

        itens = buscar_itens_venda(venda_id)
        if itens:
            print("  Itens da venda:")
            for nome_produto, tamanho, quantidade, preco_unitario in itens:
                print(f"    - {nome_produto} | Tam: {tamanho} | Qtde: {quantidade} | Unitário: R$ {preco_unitario:.2f}")
        else:
            print("  Nenhum item encontrado para esta venda.")

        print('-'*50)