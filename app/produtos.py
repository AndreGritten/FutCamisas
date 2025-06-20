#funções para gerenciar produtos
from bancoDeDados.conexao import *
import json

def adicionar_produto(nome, preco, tamanhos_dict):
    # Converter os tamanhos para JSON para armazenar no campo da tabela produtos
    tamanhos_json = json.dumps(list(tamanhos_dict.keys()))

    # Inserir na tabela produtos
    sql_produto = '''
        INSERT INTO produtos (nome, preco, tamanhos)
        VALUES (?, ?, ?)
    '''
    cursor, conexao = executar_comando_com_retorno(sql_produto, (nome, preco, tamanhos_json))

    # Pega o ID do produto recém-cadastrado
    produto_id = cursor.lastrowid

    # Inserir os tamanhos e quantidades na tabela estoque
    for tamanho, quantidade in tamanhos_dict.items():
        sql_estoque = '''
            INSERT INTO estoque (produto_id, tamanho, quantidade)
            VALUES (?, ?, ?)
        '''
        cursor.execute(sql_estoque, (produto_id, tamanho, quantidade))

    conexao.commit()
    conexao.close()

    print(f"Produto '{nome}' salvo com sucesso com ID {produto_id} e estoque registrado.")


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

        # Buscar os estoques deste produto
        sql_estoque = "SELECT tamanho, quantidade FROM estoque WHERE produto_id = ?"
        estoque = consultar(sql_estoque, (id_produto,))
        estoque_dict = {tamanho: quantidade for tamanho, quantidade in estoque}

        # Primeiro imprime tamanhos na ordem padrão (P, M, G, GG)
        for tamanho in ordem_tamanhos:
            if tamanho in tamanhos_list:
                quantidade = estoque_dict.get(tamanho, 0)
                print(f"Tam: {tamanho} ({quantidade} un)")

        # Depois tamanhos extras (se houver)
        tamanhos_extras = set(tamanhos_list) - set(ordem_tamanhos)
        for tamanho in sorted(tamanhos_extras):
            quantidade = estoque_dict.get(tamanho, 0)
            print(f"Tam: {tamanho} ({quantidade} un)")

        print('----------------------')



def editar_produto(id, novo_nome=None, novo_preco=None, novos_tamanhos=None):
    # Verificar se o produto existe
    sql_verificar = "SELECT nome, preco, tamanhos FROM produtos WHERE id = ?"
    resultado = consultar(sql_verificar, (id,))

    if not resultado:
        print(f"Produto com ID {id} não encontrado.")
        return

    nome_atual, preco_atual, tamanhos_atual_json = resultado[0]
    tamanhos_atual = json.loads(tamanhos_atual_json)

    # Atualiza lista de tamanhos se novos tamanhos forem informados
    if novos_tamanhos:
        for tamanho in novos_tamanhos.keys():
            if tamanho not in tamanhos_atual:
                tamanhos_atual.append(tamanho)

    # Atualizar a tabela produtos
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

    # Atualizar a tabela estoque (substitui a quantidade)
    if novos_tamanhos:
        for tamanho, quantidade in novos_tamanhos.items():
            # Verificar se o tamanho já existe no estoque
            sql_check = '''
                SELECT id FROM estoque
                WHERE produto_id = ? AND tamanho = ?
            '''
            existe = consultar(sql_check, (id, tamanho))

            if existe:
                # Atualiza a quantidade
                sql_update = '''
                    UPDATE estoque
                    SET quantidade = ?
                    WHERE produto_id = ? AND tamanho = ?
                '''
                executar_comando(sql_update, (quantidade, id, tamanho))
            else:
                # Insere novo tamanho
                sql_insert = '''
                    INSERT INTO estoque (produto_id, tamanho, quantidade)
                    VALUES (?, ?, ?)
                '''
                executar_comando(sql_insert, (id, tamanho, quantidade))

    print(f"Produto com ID {id} atualizado com sucesso!")





def excluir_produto(id):
    # Verificar se o produto existe
    sql_verificar = "SELECT * FROM produtos WHERE id = ?"
    resultado = consultar(sql_verificar, (id,))

    if not resultado:
        print(f"Produto com ID {id} não encontrado.")
        return

    # Excluir do estoque
    executar_comando("DELETE FROM estoque WHERE produto_id = ?", (id,))
    # Excluir do produtos
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
