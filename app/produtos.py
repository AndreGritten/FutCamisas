#funções para gerenciar produtos

produtos = []

def adicionar_produto(nome, preco, tamanhos_dict):
    produto = {
        "id": len(produtos) + 1,
        "nome": nome,
        "preco": preco,
        "tamanhos": tamanhos_dict
    }
    produtos.append(produto)
    print(f"Produto '{nome}' adicionado com sucesso! ")

def listar_produtos():
    if not produtos:
        print("Nenhum produto cadastrado.")
        return
    for p in produtos:
        print(f"[ID:{p['id']}] {p['nome']} - R$ {p['preco']}")
        for tamanho, qtd in p["tamanhos"].items():
            print(f"Tam: {tamanho} ({qtd} un)")

def editar_produto(id, novo_nome=None, novo_preco=None, novo_tamanho=None):
    for p in produtos:
        if p["id"] == id:
            if novo_nome:
                p["nome"] = novo_nome
            if novo_preco:
                p["preco"] = novo_preco
            if novo_tamanho:
                p["tamanho"] = novo_tamanho
            print("Produto atualizado.")
            return
    print("Produto não encontrado.")

def excluir_produto(id):
    global produtos
    produtos = [p for p in produtos if p["id"] != id]
    print("Produto excluído com sucesso.")
