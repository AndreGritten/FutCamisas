import sqlite3
import os
import json

def criar_banco():
    caminho_banco = os.path.join(os.path.dirname(__file__), 'futCamisas.db')
    conexao = sqlite3.connect(caminho_banco)
    cursor = conexao.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            tamanhos TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tamanho TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        );

        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('cliente', 'funcionario'))
        );

        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            data DATETIME NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('pendente', 'pago', 'enviado', 'cancelado')),
            total REAL NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );

        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            tamanho TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (venda_id) REFERENCES vendas(id),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        );
    ''')

    # Verificar se produtos já existem
    cursor.execute('SELECT COUNT(*) FROM produtos')
    quantidade = cursor.fetchone()[0]

    if quantidade == 0:
        camisas = [
            {"nome": "Camisa Flamengo 2024", "preco": 249.90, "tamanhos": {"P": 10, "M": 15, "G": 20, "GG": 5}},
            {"nome": "Camisa Palmeiras 2024", "preco": 259.90, "tamanhos": {"P": 8, "M": 12, "G": 18, "GG": 7}},
            {"nome": "Camisa Corinthians 2024", "preco": 239.90, "tamanhos": {"P": 5, "M": 10, "G": 15, "GG": 10}},
            {"nome": "Camisa São Paulo 2024", "preco": 249.90, "tamanhos": {"P": 7, "M": 13, "G": 17, "GG": 6}},
            {"nome": "Camisa Vasco 2024", "preco": 229.90, "tamanhos": {"P": 4, "M": 9, "G": 14, "GG": 8}},
            {"nome": "Camisa Grêmio 2024", "preco": 259.90, "tamanhos": {"P": 6, "M": 10, "G": 16, "GG": 7}},
            {"nome": "Camisa Internacional 2024", "preco": 249.90, "tamanhos": {"P": 5, "M": 11, "G": 15, "GG": 9}},
            {"nome": "Camisa Cruzeiro 2024", "preco": 219.90, "tamanhos": {"P": 8, "M": 14, "G": 19, "GG": 6}},
            {"nome": "Camisa Atlético-MG 2024", "preco": 239.90, "tamanhos": {"P": 7, "M": 13, "G": 17, "GG": 7}},
            {"nome": "Camisa Santos 2024", "preco": 229.90, "tamanhos": {"P": 6, "M": 12, "G": 18, "GG": 5}}
        ]

        for camisa in camisas:
            tamanhos = list(camisa["tamanhos"].keys())
            tamanhos_json = json.dumps(tamanhos)

            cursor.execute('''
                INSERT INTO produtos (nome, preco, tamanhos)
                VALUES (?, ?, ?)
            ''', (camisa["nome"], camisa["preco"], tamanhos_json))

            produto_id = cursor.lastrowid

            for tamanho, quantidade in camisa["tamanhos"].items():
                cursor.execute('''
                    INSERT INTO estoque (produto_id, tamanho, quantidade)
                    VALUES (?, ?, ?)
                ''', (produto_id, tamanho, quantidade))

        print("Produtos e estoques inseridos com sucesso!")
    else:
        print("Tabela de produtos já possui dados cadastrados.")

    # Inserir usuários se não existirem
    cursor.execute('SELECT COUNT(*) FROM usuarios')
    quantidade_usuarios = cursor.fetchone()[0]

    if quantidade_usuarios == 0:
        usuarios = [
            {"nome": "João Silva", "cpf": "12345678901", "email": "joao.silva@email.com", "senha": "senha123", "tipo": "cliente"},
            {"nome": "Maria Oliveira", "cpf": "23456789012", "email": "maria.oliveira@email.com", "senha": "senha456", "tipo": "cliente"},
            {"nome": "Carlos Pereira", "cpf": "34567890123", "email": "carlos.pereira@email.com", "senha": "senha789", "tipo": "funcionario"},
            {"nome": "Ana Souza", "cpf": "45678901234", "email": "ana.souza@email.com", "senha": "senha321", "tipo": "cliente"},
            {"nome": "Pedro Santos", "cpf": "56789012345", "email": "pedro.santos@email.com", "senha": "senha654", "tipo": "funcionario"},
            {"nome": "Luciana Costa", "cpf": "67890123456", "email": "luciana.costa@email.com", "senha": "senha987", "tipo": "cliente"},
            {"nome": "Felipe Rocha", "cpf": "78901234567", "email": "felipe.rocha@email.com", "senha": "senha111", "tipo": "funcionario"},
            {"nome": "Patrícia Lima", "cpf": "89012345678", "email": "patricia.lima@email.com", "senha": "senha222", "tipo": "cliente"},
            {"nome": "Ricardo Almeida", "cpf": "90123456789", "email": "ricardo.almeida@email.com", "senha": "senha333", "tipo": "funcionario"},
            {"nome": "Sandra Martins", "cpf": "01234567890", "email": "sandra.martins@email.com", "senha": "senha444", "tipo": "cliente"}
        ]

        for user in usuarios:
            cursor.execute('''
                INSERT INTO usuarios (nome, cpf, email, senha, tipo)
                VALUES (?, ?, ?, ?, ?)
            ''', (user["nome"], user["cpf"], user["email"], user["senha"], user["tipo"]))

        print("Usuários inseridos com sucesso!")
    else:
        print("Tabela de usuários já possui dados cadastrados.")

    conexao.commit()
    conexao.close()
    print(f"Banco de dados e tabelas criados com sucesso em {caminho_banco}!")


if __name__ == "__main__":
    criar_banco()
