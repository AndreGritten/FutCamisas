#funções para gerenciar produtos

produtos = []

def adicionar_produto(nome, preco, tamanho):
    produto = {
        "id": len(produtos) + 1,
        "nome": nome,
        "preco": preco,
        "tamanho": tamanho
    }
    produtos.append(produto)
    print(f"Produto '{nome}' adicionado com sucesso! ")

def listar_produtos():
    if not produtos:
        print("Nenhum produto cadastrado.")
        return
    for p in produtos:
        print(f"[{p['id']}] {p['nome']} - R$ {p['preco']} - Tam: {p['tamanho']}")

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
