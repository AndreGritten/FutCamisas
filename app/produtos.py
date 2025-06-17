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
    sql = "SELECT id, nome, preco, tamanhos FROM produtos WHERE nome = 'Camisa Corinthians 2024'"
    resultados = consultar(sql)
    
    if not resultados:
        print("Nenhum produto cadastrado.")
        return
    
    for linha in resultados:
        id_produto, nome, preco, tamanhos_json = linha
        tamanhos_dict = json.loads(tamanhos_json)
        print(f"[ID:{id_produto}] {nome} - R$ {preco}")
        for tamanho, qtd in tamanhos_dict.items():
            print(f"Tam: {tamanho} ({qtd} un)")
        print('----------------------')

def editar_produto(id, novo_nome=None, novo_preco=None, novos_tamanhos=None):
    # Verificar se o produto existe
    sql_verificar = "SELECT * FROM produtos WHERE id = ?"
    resultado = consultar(sql_verificar, (id,))
    

    if not resultado:
        print(f"Produto com ID {id} não encontrado.")
        return

    # Construir os campos que serão atualizados
    campos = []
    parametros = []

    if novo_nome:
        campos.append("nome = ?")
        parametros.append(novo_nome)
    if novo_preco is not None:
        campos.append("preco = ?")
        parametros.append(novo_preco)
    if novos_tamanhos:
        tamanhos_json = json.dumps(novos_tamanhos)
        campos.append("tamanhos = ?")
        parametros.append(tamanhos_json)

    if not campos:
        print("Nenhuma informação para atualizar.")
        return

    parametros.append(id)  # ID para o WHERE

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

