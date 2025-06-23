from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json
import sqlite3
from datetime import datetime 
from .bancoDeDados.conexao import conectar, executar_comando, consultar, executar_comando_com_retorno
from .produtos import adicionar_produto, editar_produto, excluir_produto
from .usuarios import register_user, login_user, edit_user, delete_user, list_users 
app = Flask(__name__)

CORS(app)


CAMINHO_BANCO = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'produtos.db')


def criar_banco():
    conexao = None 
    try:
        conexao = sqlite3.connect(CAMINHO_BANCO)
        cursor = conexao.cursor()

       
        conexao.execute("PRAGMA foreign_keys = ON;")

        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                tamanhos TEXT NOT NULL -- Armazena JSON string com os nomes dos tamanhos disponíveis (e.g., "['P', 'M']")
            );

            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tamanho TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE
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
                data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
                FOREIGN KEY (venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
                FOREIGN KEY (produto_id) REFERENCES produtos(id)
            );
        ''')
        conexao.commit() 
        cursor.execute('SELECT COUNT(*) FROM produtos')
        quantidade_produtos = cursor.fetchone()[0]

        if quantidade_produtos == 0:
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
               
                tamanhos_disponiveis_para_produto = list(camisa["tamanhos"].keys())
                tamanhos_json_db = json.dumps(tamanhos_disponiveis_para_produto)

                cursor.execute('''
                    INSERT INTO produtos (nome, preco, tamanhos)
                    VALUES (?, ?, ?)
                ''', (camisa["nome"], camisa["preco"], tamanhos_json_db))
                produto_id = cursor.lastrowid 
                

                for tamanho, quantidade in camisa["tamanhos"].items():
                    cursor.execute('''
                        INSERT INTO estoque (produto_id, tamanho, quantidade)
                        VALUES (?, ?, ?)
                    ''', (produto_id, tamanho, quantidade))
            print("Produtos e estoques iniciais inseridos com sucesso!")
        else:
            print("Tabela de produtos já possui dados cadastrados. Pulando inserção inicial.")

       
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
            print("Usuários iniciais inseridos com sucesso!")
        else:
            print("Tabela de usuários já possui dados cadastrados. Pulando inserção inicial.")

        conexao.commit() 
        
        print(f"Banco de dados e tabelas criados/verificados com sucesso em {CAMINHO_BANCO}!")

    except sqlite3.Error as er:
        print(f"Erro SQLite ao criar banco ou inserir dados: {er}")
        if conexao:
            conexao.rollback() 
    finally:
        if conexao:
            conexao.close()


@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    
    sql = "SELECT id, nome, preco, tamanhos FROM produtos"
    resultados_produtos = consultar(sql) 

    produtos_formatados = []
    for id_produto, nome, preco, tamanhos_json_db in resultados_produtos:
      
        estoque_sql = "SELECT tamanho, quantidade FROM estoque WHERE produto_id = ?"
        estoque_resultados = consultar(estoque_sql, (id_produto,))
        estoque_real_dict = {tamanho: qtd for tamanho, qtd in estoque_resultados}

        produtos_formatados.append({
            "id": id_produto,
            "nome": nome,
            "preco": preco,
            "tamanhos": estoque_real_dict 
        })
    return jsonify(produtos_formatados)


@app.route('/api/produtos', methods=['POST'])
def add_new_produto():
    """
    Adiciona um novo produto ao banco de dados e seu estoque.
    Espera um JSON com 'nome', 'preco' e 'tamanhos' (ex: {"P": 10, "M": 5}).
    """
    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados inválidos"}), 400

    nome = data.get('nome')
    preco = data.get('preco')
    tamanhos_dict = data.get('tamanhos') 

    if not all([nome, preco, tamanhos_dict]):
        return jsonify({"message": "Nome, preço e tamanhos são obrigatórios"}), 400
    if not isinstance(tamanhos_dict, dict) or not tamanhos_dict:
        return jsonify({"message": "Tamanhos devem ser um dicionário não vazio"}), 400

    try:
        adicionar_produto(nome, preco, tamanhos_dict) 
        return jsonify({"message": f"Produto '{nome}' adicionado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"message": f"Erro ao adicionar produto: {str(e)}"}), 500


@app.route('/api/produtos/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    
    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados inválidos"}), 400

    novo_nome = data.get('nome')
    novo_preco = data.get('preco')
    novos_tamanhos = data.get('tamanhos')

    try:
        
        success, message = editar_produto(produto_id, novo_nome, novo_preco, novos_tamanhos)
        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": message}), 404
    except Exception as e:
        return jsonify({"message": f"Erro ao atualizar produto: {str(e)}"}), 500


@app.route('/api/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
   
    try:
        
        success, message = excluir_produto(produto_id)
        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": message}), 404 #caso o produto não seja encontrado
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir produto: {str(e)}"}), 500


@app.route('/api/usuarios/registrar', methods=['POST'])
def api_register_user():
   
    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados inválidos"}), 400

    nome = data.get('nome')
    cpf = data.get('cpf')
    email = data.get('email')
    senha = data.get('senha')
    tipo = data.get('tipo', 'cliente') 

    if not all([nome, cpf, email, senha]):
        return jsonify({"message": "Nome, CPF, email e senha são obrigatórios"}), 400

   
    success, message = register_user(nome, email, senha, cpf, tipo)
    if success:
        return jsonify({"message": message}), 201
    else:
        return jsonify({"message": message}), 409 


@app.route('/api/usuarios/login', methods=['POST'])
def api_user_login():
   
    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados inválidos"}), 400

    email = data.get('email')
    senha = data.get('senha')

    if not all([email, senha]):
        return jsonify({"message": "Email e senha são obrigatórios"}), 400

   
    success, message, user_data = login_user(email, senha)
    if success:
        
        return jsonify({"message": message, "user": {"id": user_data[0], "name": user_data[1], "type": user_data[2]}}), 200
    else:
        return jsonify({"message": message}), 401


@app.route('/api/usuarios', methods=['GET'])
def api_get_users():
   
    users_from_db = list_users()
    users_list_for_api = [{"id": user[0], "name": user[1], "cpf": user[2], "email": user[3], "type": user[4]} for user in users_from_db]
    return jsonify(users_list_for_api), 200


@app.route('/api/usuarios/<id_or_email>', methods=['PUT'])
def api_update_user(id_or_email):
   
    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados inválidos"}), 400

    current_password = data.get('password') 
    new_name = data.get('new_name')
    new_email = data.get('new_email')
    new_password = data.get('new_password')
    new_tipo = data.get('new_tipo')

    try:

        success, message = edit_user(
            id=int(id_or_email) if isinstance(id_or_email, str) and id_or_email.isdigit() else None,
            email=id_or_email if not (isinstance(id_or_email, str) and id_or_email.isdigit()) else None,
            password=current_password,
            new_name=new_name if new_name else None,
            new_email=new_email if new_email else None,
            new_password=new_password if new_password else None,
            new_tipo=new_tipo if new_tipo else None
        )
        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": message}), 400 
    except Exception as e:
        return jsonify({"message": f"Erro ao atualizar usuário: {str(e)}"}), 500

@app.route('/api/usuarios/<id_or_email>', methods=['DELETE'])
def api_delete_user(id_or_email):
  
    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({"message": "Senha é obrigatória para exclusão"}), 400

    password_confirmation = data.get('password')

    try:

        success, message = delete_user(id_or_email, password=password_confirmation)
        if success:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"message": message}), 404 
    except Exception as e:
        return jsonify({"message": f"Erro ao excluir usuário: {str(e)}"}), 500

@app.route('/api/vendas', methods=['POST'])
def api_salvar_venda():
    
    data = request.get_json()
    if not data:
        return jsonify({"message": "Dados inválidos"}), 400

    usuario_id = data.get('usuario_id')
    carrinho = data.get('carrinho') 

    if not all([usuario_id, carrinho]):
        return jsonify({"message": "ID do usuário e carrinho são obrigatórios"}), 400
    if not isinstance(carrinho, list) or not carrinho:
        return jsonify({"message": "Carrinho deve ser uma lista não vazia de itens"}), 400

    for item in carrinho:
        produto_id = item.get('produto_id')
        tamanho = item.get('tamanho')
        quantidade = item.get('quantidade')
        if not all([produto_id, tamanho, quantidade]):
            return jsonify({"message": "Item do carrinho incompleto"}), 400

        from .vendas import verificar_estoque 
        if not verificar_estoque(produto_id, tamanho, quantidade):
            return jsonify({"message": f"Estoque insuficiente para o produto {produto_id} (Tam: {tamanho})"}), 400

    try:
        from .vendas import salvar_venda
        venda_id = salvar_venda(usuario_id, carrinho)
        if venda_id:
            return jsonify({"message": f"Venda {venda_id} criada com sucesso!"}), 201
        else:
            return jsonify({"message": "Falha ao criar venda"}), 500
    except Exception as e:
        return jsonify({"message": f"Erro ao criar venda: {str(e)}"}), 500

@app.route('/api/vendas/usuario/<int:usuario_id>', methods=['GET'])
def api_buscar_vendas_usuario(usuario_id):
    
    from .vendas import buscar_vendas_usuario, buscar_itens_venda
    vendas_usuario = buscar_vendas_usuario(usuario_id)

    vendas_formatadas = []
    for venda_id, data, status, total in vendas_usuario:
        itens = buscar_itens_venda(venda_id)
        itens_formatados = []
        for nome_produto, tamanho, quantidade, preco_unitario in itens:
            itens_formatados.append({
                "nome": nome_produto,
                "tamanho": tamanho,
                "quantidade": quantidade,
                "preco_unitario": preco_unitario
            })
        vendas_formatadas.append({
            "id": venda_id,
            "data": data,
            "status": status,
            "total": total,
            "itens": itens_formatados
        })
    return jsonify(vendas_formatadas), 200

@app.route('/api/vendas/todas', methods=['GET'])
def api_listar_todas_vendas():
   
    from .vendas import listar_todas_vendas, buscar_itens_venda 
    todas_vendas = listar_todas_vendas()

    vendas_formatadas = []
    for venda_id, data, status, total, nome_usuario, cpf_usuario, email_usuario in todas_vendas:
        itens = buscar_itens_venda(venda_id)
        itens_formatados = []
        for nome_produto, tamanho, quantidade, preco_unitario in itens:
            itens_formatados.append({
                "nome": nome_produto,
                "tamanho": tamanho,
                "quantidade": quantidade,
                "preco_unitario": preco_unitario
            })
        vendas_formatadas.append({
            "id": venda_id,
            "data": data,
            "status": status,
            "total": total,
            "usuario": {"nome": nome_usuario, "cpf": cpf_usuario, "email": email_usuario},
            "itens": itens_formatados
        })
    return jsonify(vendas_formatadas), 200
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == '__main__':
    print("Verificando/criando banco de dados...")
    criar_banco()
    print("Banco de dados pronto.")
    print("Iniciando servidor Flask...")
    app.run(debug=True, port=5000)