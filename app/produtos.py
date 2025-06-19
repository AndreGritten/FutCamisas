#funções para gerenciar produtos
from bancoDeDados.conexao import *
import json

def adicionar_produto(nome, preco, tamanhos_dict):

    tamanhos_json = json.dumps(tamanhos_dict)

    sql = '''
        INSERT INTO produtos (nome, preco, tamanhos)
        VALUES (?, ?, ?)
    '''
    parametros = (nome, preco, tamanhos_json)
    executar_comando(sql, parametros)
    print(f"Produto '{nome}' salvo no banco com sucesso!")

def listar_produtos():
    sql = "SELECT id, nome, preco, tamanhos FROM produtos"
    resultados = consultar(sql)
    
    if not resultados:
        print("Nenhum produto cadastrado.")
        return
    
    ordem_tamanhos = ["P", "M", "G", "GG"]  # Ordem desejada
    
    for linha in resultados:
        id_produto, nome, preco, tamanhos_json = linha
        tamanhos_dict = json.loads(tamanhos_json)
        
        print(f"[ID:{id_produto}] {nome} - R$ {preco}")
        
        # Primeiro imprime na ordem padrão (P, M, G, GG)
        for tamanho in ordem_tamanhos:
            if tamanho in tamanhos_dict:
                print(f"Tam: {tamanho} ({tamanhos_dict[tamanho]} un)")

        # Depois imprime tamanhos extras fora da ordem padrão, se houver
        tamanhos_extras = set(tamanhos_dict.keys()) - set(ordem_tamanhos)
        for tamanho in sorted(tamanhos_extras):
            print(f"Tam: {tamanho} ({tamanhos_dict[tamanho]} un)")

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

    # Se novos tamanhos foram passados, somar aos existentes
    if novos_tamanhos:
        for tamanho, quantidade in novos_tamanhos.items():
            if tamanho in tamanhos_atual:
                tamanhos_atual[tamanho] += quantidade
            else:
                tamanhos_atual[tamanho] = quantidade

    # Construir os campos para atualizar
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

    if not campos:
        print("Nenhuma informação para atualizar.")
        return

    parametros.append(id)  # ID no WHERE

    sql = f'''
        UPDATE produtos
        SET {', '.join(campos)}
        WHERE id = ?
    '''

    executar_comando(sql, tuple(parametros))
    print(f"Produto com ID {id} atualizado com sucesso!")



def excluir_produto(id):
    # Verificar se o produto existe
    sql_verificar = "SELECT * FROM produtos WHERE id = ?"
    resultado = consultar(sql_verificar, (id,))

    if not resultado:
        print(f"Produto com ID {id} não encontrado.")
        return

    # Executar exclusão
    sql = "DELETE FROM produtos WHERE id = ?"
    executar_comando(sql, (id,))
    print(f"Produto com ID {id} excluído com sucesso!")


def adicionar_quantidade_produto():
    listar_produtos()
    try:
        id_produto = int(input("Informe o ID do produto para adicionar quantidade: "))
    except ValueError:
        print("ID inválido.")
        return
    
    sql_buscar = "SELECT tamanhos FROM produtos WHERE id = ?"
    resultado = consultar(sql_buscar, (id_produto,))

    if not resultado:
        print(f"Produto com ID {id_produto} não encontrado.")
        return

    tamanhos_json = resultado[0][0]
    tamanhos_dict = json.loads(tamanhos_json)

    tamanho = input("Informe o tamanho que deseja adicionar (ex.: P, M, G): ").upper()
    try:
        quantidade_adicional = int(input(f"Quantidade que deseja adicionar no tamanho {tamanho}: "))
    except ValueError:
        print("Quantidade inválida.")
        return

    if tamanho in tamanhos_dict:
        tamanhos_dict[tamanho] += quantidade_adicional
    else:
        tamanhos_dict[tamanho] = quantidade_adicional

    tamanhos_json_novo = json.dumps(tamanhos_dict)

    sql_update = '''
        UPDATE produtos
        SET tamanhos = ?
        WHERE id = ?
    '''
    parametros = (tamanhos_json_novo, id_produto)

    executar_comando(sql_update, parametros)

    print(f"Quantidade adicionada com sucesso no produto ID {id_produto}, tamanho {tamanho}.")
