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
            tamanho TEXT NOT NULL, -- Ex.: P, M, G
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

    cursor.execute('SELECT COUNT(*) FROM produtos')
    quantidade = cursor.fetchone()[0]

    if quantidade == 0:
        # Dados das camisas
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
            tamanhos_json = json.dumps(camisa["tamanhos"])
            cursor.execute('''
                INSERT INTO produtos (nome, preco, tamanhos)
                VALUES (?, ?, ?)
            ''', (camisa["nome"], camisa["preco"], tamanhos_json))

        print("Produtos inseridos com sucesso!")
    else:
        print("Tabela já possui produtos cadastrados.")

    conexao.commit()
    conexao.close()
    print(f"Banco de dados e tabela criados com sucesso em {caminho_banco}!")

if __name__ == "__main__":
    criar_banco()
