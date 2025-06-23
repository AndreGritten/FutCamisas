import json
from .bancoDeDados.conexao import executar_comando, consultar, executar_comando_com_retorno

def adicionar_produto(nome, preco, tamanhos_dict):

    tamanhos_disponiveis_json = json.dumps(list(tamanhos_dict.keys()))

    sql_produto = '''
        INSERT INTO produtos (nome, preco, tamanhos)
        VALUES (?, ?, ?)
    '''

    cursor, conexao = executar_comando_com_retorno(sql_produto, (nome, preco, tamanhos_disponiveis_json))

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
        return False, "Produto não encontrado."

    nome_atual, preco_atual, tamanhos_atual_json = resultado[0]
    tamanhos_disponiveis_lista = json.loads(tamanhos_atual_json) 

    conexao = conectar()
    cursor = conexao.cursor()

    try:
       
        campos_produto = []
        parametros_produto = []

        if novo_nome is not None:
            campos_produto.append("nome = ?")
            parametros_produto.append(novo_nome)
        if novo_preco is not None:
            campos_produto.append("preco = ?")
            parametros_produto.append(novo_preco)

        if novos_tamanhos:
            
            for tamanho_novo in novos_tamanhos.keys():
                if tamanho_novo not in tamanhos_disponiveis_lista:
                    tamanhos_disponiveis_lista.append(tamanho_novo)
            campos_produto.append("tamanhos = ?")
            parametros_produto.append(json.dumps(tamanhos_disponiveis_lista))

        if campos_produto: 
            sql_update_produto = f'''
                UPDATE produtos
                SET {', '.join(campos_produto)}
                WHERE id = ?
            '''
            parametros_produto.append(id)
            cursor.execute(sql_update_produto, tuple(parametros_produto))

        if novos_tamanhos:
            for tamanho, quantidade in novos_tamanhos.items():
                sql_check_estoque = '''
                    SELECT id FROM estoque
                    WHERE produto_id = ? AND tamanho = ?
                '''
                existe_estoque = consultar(sql_check_estoque, (id, tamanho)) # Usa consultar global

                if existe_estoque:
                    sql_update_estoque = '''
                        UPDATE estoque
                        SET quantidade = ?
                        WHERE produto_id = ? AND tamanho = ?
                    '''
                    cursor.execute(sql_update_estoque, (quantidade, id, tamanho))
                else:
                    sql_insert_estoque = '''
                        INSERT INTO estoque (produto_id, tamanho, quantidade)
                        VALUES (?, ?, ?)
                    '''
                    cursor.execute(sql_insert_estoque, (id, tamanho, quantidade))

        conexao.commit() 
        print(f"Produto com ID {id} atualizado com sucesso!")
        return True, "Produto atualizado com sucesso!"

    except sqlite3.Error as e:
        conexao.rollback() 
        print(f"Erro ao atualizar produto: {e}")
        return False, f"Erro ao atualizar produto: {e}"
    finally:
        conexao.close()


def excluir_produto(id):

    sql_verificar = "SELECT id FROM produtos WHERE id = ?"
    resultado = consultar(sql_verificar, (id,))

    if not resultado:
        print(f"Produto com ID {id} não encontrado.")
        return False, "Produto não encontrado."

    try:
       
        executar_comando("DELETE FROM estoque WHERE produto_id = ?", (id,))
        
        executar_comando("DELETE FROM produtos WHERE id = ?", (id,))

        print(f"Produto com ID {id} e seu estoque foram excluídos com sucesso!")
        return True, "Produto excluído com sucesso!"
    except sqlite3.Error as e:
        print(f"Erro ao excluir produto: {e}")
        return False, f"Erro ao excluir produto: {e}"


def listar_produtos():
   
    sql = "SELECT id, nome, preco, tamanhos FROM produtos"
    resultados = consultar(sql)

    if not resultados:
        print("Nenhum produto cadastrado.")
        return

    ordem_tamanhos = ["P", "M", "G", "GG"] 

    for linha in resultados:
        id_produto, nome, preco, tamanhos_json = linha
        tamanhos_list = json.loads(tamanhos_json) 

        print(f"[ID:{id_produto}] {nome} - R$ {preco:.2f}")

        sql_estoque = "SELECT tamanho, quantidade FROM estoque WHERE produto_id = ?"
        estoque = consultar(sql_estoque, (id_produto,))
        estoque_dict = {tamanho: quantidade for tamanho, quantidade in estoque}

        for tamanho in ordem_tamanhos:
            if tamanho in tamanhos_list: 
                quantidade = estoque_dict.get(tamanho, 0) 
                print(f"  Tam: {tamanho} ({quantidade} un)")

        
        tamanhos_extras = set(tamanhos_list) - set(ordem_tamanhos)
        for tamanho in sorted(tamanhos_extras):
            quantidade = estoque_dict.get(tamanho, 0)
            print(f"  Tam: {tamanho} ({quantidade} un)")

        print('----------------------')


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

        print(f"[ID:{id_produto}] {nome} - R$ {preco:.2f}")

        sql_estoque = "SELECT tamanho, quantidade FROM estoque WHERE produto_id = ?"
        estoque = consultar(sql_estoque, (id_produto,))
        estoque_dict = {tamanho: quantidade for tamanho, quantidade in estoque}

        for tamanho in tamanhos_list:
            quantidade = estoque_dict.get(tamanho, 0)
            print(f"  Tam: {tamanho} ({quantidade} un)")

        print('----------------------')


def filtrar_produtos_por_preco(preco_min, preco_max):
    
    sql = "SELECT id, nome, preco, tamanhos FROM produtos WHERE preco BETWEEN ? AND ?"
    resultados = consultar(sql, (preco_min, preco_max))

    if not resultados:
        print(f"Nenhum produto encontrado na faixa de preço de R$ {preco_min:.2f} até R$ {preco_max:.2f}.")
        return

    print(f"\nProdutos com preço entre R$ {preco_min:.2f} e R$ {preco_max:.2f}:")
    for id_produto, nome, preco, tamanhos_json in resultados:
        tamanhos_list = json.loads(tamanhos_json)

        print(f"[ID:{id_produto}] {nome} - R$ {preco:.2f}")

        sql_estoque = "SELECT tamanho, quantidade FROM estoque WHERE produto_id = ?"
        estoque = consultar(sql_estoque, (id_produto,))
        estoque_dict = {tamanho: quantidade for tamanho, quantidade in estoque}

        for tamanho in tamanhos_list:
            quantidade = estoque_dict.get(tamanho, 0)
            print(f"  Tam: {tamanho} ({quantidade} un)")

        print('----------------------')


def adicionar_produto_interativo():
    nome = input("Nome do produto: ").strip()
    preco = float(input("Preço do produto: R$ "))

    tamanhos_dict = {}
    while True:
        tamanho = input("Informe um tamanho (ex.: P, M, G, ou Enter para finalizar): ").upper().strip()
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


def editar_produto_interativo():
    while True:
        listar_produtos()
        id_input = input("ID do produto para editar (ou pressione Enter para sair): ").strip()
        if id_input == "":
            break
        try:
            id_produto = int(id_input)
        except ValueError:
            print("ID inválido. Digite um número válido.")
            continue

        novo_nome = input("Novo nome (pressione Enter para manter o atual): ").strip()
        novo_preco_input = input("Novo preço (pressione Enter para manter o atual): ").strip()

        novo_tamanhos_dict = {}

        while True:
            tamanho = input("Informe um tamanho (ex.: P, M, G, ou Enter para finalizar tamanhos): ").upper().strip()
            if tamanho == "":
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
        if novo_preco_input != "":
            try:
                novo_preco = float(novo_preco_input)
            except ValueError:
                print("Preço inválido. Não foi alterado.")

        sucesso, mensagem = editar_produto(
            id_produto,
            novo_nome if novo_nome != "" else None,
            novo_preco,
            novo_tamanhos_dict if novo_tamanhos_dict else None
        )
        print(mensagem)


def excluir_produto_interativo():
    listar_produtos()
    try:
        id_produto = int(input("ID do produto para excluir: "))
    except ValueError:
        print("ID inválido.")
        return

    sucesso, mensagem = excluir_produto(id_produto)
    print(mensagem)