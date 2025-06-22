from bancoDeDados.conexao import *
import json

def adicionar_produto_interativo():
    nome = input("Nome do produto: ")
    preco = float(input("Preço do produto: R$ "))

    tamanhos_dict = {}
    while True:
        tamanho = input("Informe um tamanho (ou Enter para finalizar): ").upper()
        if tamanho == "":
            break
        try:
            quantidade = int(input(f"Quantidade para tamanho {tamanho}: "))
        except ValueError:
            print("Quantidade inválida. Informe um número inteiro.")
            continue
        if tamanho in tamanhos_dict:
            tamanhos_dict[tamanho] += quantidade
        else:
            tamanhos_dict[tamanho] = quantidade

    adicionar_produto(nome, preco, tamanhos_dict)


def listar_produtos():
    sql = "SELECT id, nome, preco, tamanhos FROM produtos"
    resultados = consultar(sql)

    if not resultados:
        print("Nenhum produto cadastrado.")
        return

    ordem_tamanhos = ["P", "M", "G", "GG"]  # Ordem desejada

    for linha in resultados:
        id_produto, nome, preco, tamanhos_json = linha
        tamanhos_list = json.loads(tamanhos_json)

        print(f"[ID:{id_produto}] {nome} - R$ {preco}")

        sql_estoque = "SELECT tamanho, quantidade FROM estoque WHERE produto_id = ?"
        estoque = consultar(sql_estoque, (id_produto,))
        estoque_dict = {tamanho: quantidade for tamanho, quantidade in estoque}

        for tamanho in ordem_tamanhos:
            if tamanho in tamanhos_list:
                quantidade = estoque_dict.get(tamanho, 0)
                print(f"Tam: {tamanho} ({quantidade} un)")

        tamanhos_extras = set(tamanhos_list) - set(ordem_tamanhos)
        for tamanho in sorted(tamanhos_extras):
            quantidade = estoque_dict.get(tamanho, 0)
            print(f"Tam: {tamanho} ({quantidade} un)")

        print('----------------------')


def editar_produto_interativo():
    while True:
        listar_produtos()
        id_input = input("ID do produto para editar (ou pressione Enter para sair): ")
        if id_input.strip() == "":
            break
        try:
            id_produto = int(id_input)
        except ValueError:
            print("ID inválido. Digite um número válido.")
            continue

        novo_nome = input("Novo nome (pressione Enter para manter o atual): ")
        novo_preco_input = input("Novo preço (pressione Enter para manter o atual): ")

        novo_tamanhos_dict = {}

        while True:
            tamanho = input("Informe um tamanho (ou pressione Enter para finalizar tamanhos): ").upper()
            if tamanho.strip() == "":
                break
            try:
                quantidade = int(input(f"Quantidade para tamanho {tamanho}: "))
            except ValueError:
                print("Quantidade inválida. Informe um número inteiro.")
                continue

            if tamanho in novo_tamanhos_dict:
                novo_tamanhos_dict[tamanho] += quantidade
            else:
                novo_tamanhos_dict[tamanho] = quantidade

            mais_tamanhos = input("Deseja adicionar mais quantidades para outro tamanho? (S/N): ").strip().upper()
            if mais_tamanhos != "S":
                break

        novo_preco = None
        if novo_preco_input.strip() != "":
            try:
                novo_preco = float(novo_preco_input)
            except ValueError:
                print("Preço inválido. Não foi alterado.")

        editar_produto(
            id_produto,
            novo_nome if novo_nome.strip() != "" else None,
            novo_preco,
            novo_tamanhos_dict if novo_tamanhos_dict else None
        )

        continuar = input("\nDeseja editar outro produto? (pressione Enter para sair ou qualquer tecla para continuar): ")
        if continuar.strip() == "":
            break


def excluir_produto_interativo():
    try:
        id_produto = int(input("ID do produto para excluir: "))
    except ValueError:
        print("ID inválido.")
        return

    excluir_produto(id_produto)


def filtrar_produtos_por_nome_interativo():
    nome = input("Digite o nome do time ou parte do nome para buscar: ")
    filtrar_produtos_por_nome(nome)


def filtrar_produtos_por_preco_interativo():
    try:
        preco_min = float(input("Digite o preço mínimo: R$ "))
        preco_max = float(input("Digite o preço máximo: R$ "))
        filtrar_produtos_por_preco(preco_min, preco_max)
    except ValueError:
        print("Preço inválido.")


# Funções que fazem operação no banco (sem interação)

def adicionar_produto(nome, preco, tamanhos_dict):
    tamanhos_json = json.dumps(list(tamanhos_dict.keys()))

    sql_produto = '''
        INSERT INTO produtos (nome, preco, tamanhos)
        VALUES (?, ?, ?)
    '''
    cursor, conexao = executar_comando_com_retorno(sql_produto, (nome, preco, tamanhos_json))

    produto_id = cursor.lastrowid

    for tamanho, quantidade in tamanhos_dict.items():
        sql_estoque = '''
            INSERT INTO estoque (produto_id, tamanho, quantidade)
            VALUES (?, ?, ?)
        '''
        cursor.execute(sql_estoque, (produto_id, tamanho, quantidade))

    conexao.commit()
    conexao.close()

    print(f"Produto '{nome}' salvo com sucesso com ID {produto_id} e estoque registrado.")


def editar_produto(id, novo_nome=None, novo_preco=None, novos_tamanhos=None):
    sql_verificar = "SELECT nome, preco, tamanhos FROM produtos WHERE id = ?"
    resultado = consultar(sql_verificar, (id,))

    if not resultado:
        print(f"Produto com ID {id} não encontrado.")
        return

    nome_atual, preco_atual, tamanhos_atual_json = resultado[0]
    tamanhos_atual = json.loads(tamanhos_atual_json)

    if novos_tamanhos:
        for tamanho in novos_tamanhos.keys():
            if tamanho not in tamanhos_atual:
                tamanhos_atual.append(tamanho)

    campos = []
    parametros = []

    if novo_nome:
        campos.append("nome = ?")
        parametros.append(novo_nome)
    if novo_preco is not None:
        campos.append("preco = ?")
        parametros.append(novo_preco)
    if novos_tamanhos:
        tamanhos_json = json.dumps(tamanhos_atual)
        campos.append("tamanhos = ?")
        parametros.append(tamanhos_json)

    if campos:
        sql = f'''
            UPDATE produtos
            SET {', '.join(campos)}
            WHERE id = ?
        '''
        parametros.append(id)
        executar_comando(sql, tuple(parametros))

    if novos_tamanhos:
        for tamanho, quantidade in novos_tamanhos.items():
            sql_check = '''
                SELECT id FROM estoque
                WHERE produto_id = ? AND tamanho = ?
            '''
            existe = consultar(sql_check, (id, tamanho))

            if existe:
                sql_update = '''
                    UPDATE estoque
                    SET quantidade = ?
                    WHERE produto_id = ? AND tamanho = ?
                '''
                executar_comando(sql_update, (quantidade, id, tamanho))
            else:
                sql_insert = '''
                    INSERT INTO estoque (produto_id, tamanho, quantidade)
                    VALUES (?, ?, ?)
                '''
                executar_comando(sql_insert, (id, tamanho, quantidade))

    print(f"Produto com ID {id} atualizado com sucesso!")


def excluir_produto(id):
    sql_verificar = "SELECT * FROM produtos WHERE id = ?"
    resultado = consultar(sql_verificar, (id,))

    if not resultado:
        print(f"Produto com ID {id} não encontrado.")
        return

    executar_comando("DELETE FROM estoque WHERE produto_id = ?", (id,))
    executar_comando("DELETE FROM produtos WHERE id = ?", (id,))

    print(f"Produto com ID {id} e seu estoque foram excluídos com sucesso!")


def filtrar_produtos_por_nome(nome_busca):
    sql = "SELECT id, nome, preco, tamanhos FROM produtos WHERE nome LIKE ?"
    parametro = f"%{nome_busca}%"
    resultados = consultar(sql, (parametro,))

    if not resultados:
        print(f"Nenhum produto encontrado com '{nome_busca}'.")
        return

    print(f"\nProdutos que contêm '{nome_busca}':")
    for id_produto, nome, preco, tamanhos_json in resultados:
        tamanhos_list = json.loads(tamanhos_json)

        print(f"[ID:{id_produto}] {nome} - R$ {preco}")

        sql_estoque = "SELECT tamanho, quantidade FROM estoque WHERE produto_id = ?"
        estoque = consultar(sql_estoque, (id_produto,))
        estoque_dict = {tamanho: quantidade for tamanho, quantidade in estoque}

        for tamanho in tamanhos_list:
            quantidade = estoque_dict.get(tamanho, 0)
            print(f"Tam: {tamanho} ({quantidade} un)")

        print('----------------------')


def filtrar_produtos_por_preco(preco_min, preco_max):
    sql = "SELECT id, nome, preco, tamanhos FROM produtos WHERE preco BETWEEN ? AND ?"
    resultados = consultar(sql, (preco_min, preco_max))

    if not resultados:
        print(f"Nenhum produto encontrado na faixa de preço de R$ {preco_min} até R$ {preco_max}.")
        return

    print(f"\nProdutos com preço entre R$ {preco_min} e R$ {preco_max}:")
    for id_produto, nome, preco, tamanhos_json in resultados:
        tamanhos_list = json.loads(tamanhos_json)

        print(f"[ID:{id_produto}] {nome} - R$ {preco}")

        sql_estoque = "SELECT tamanho, quantidade FROM estoque WHERE produto_id = ?"
        estoque = consultar(sql_estoque, (id_produto,))
        estoque_dict = {tamanho: quantidade for tamanho, quantidade in estoque}

        for tamanho in tamanhos_list:
            quantidade = estoque_dict.get(tamanho, 0)
            print(f"Tam: {tamanho} ({quantidade} un)")

        print('----------------------')