from bancoDeDados.conexao import *
import sqlite3

# --- Funções de lógica (somente banco e regras) ---

def registrar_usuario(nome, cpf, email, senha, tipo):
    try:
        sql = '''
            INSERT INTO usuarios (nome, cpf, email, senha, tipo)
            VALUES (?, ?, ?, ?, ?)
        '''
        executar_comando(sql, (nome, cpf, email, senha, tipo))
        return True, f"Usuário '{nome}' cadastrado com sucesso!"
    except sqlite3.IntegrityError as e:
        return False, f"Erro ao cadastrar usuário: {e}"

def verificar_login(email, senha):
    sql = "SELECT * FROM usuarios WHERE email = ? AND senha = ?"
    resultado = consultar(sql, (email, senha))
    return bool(resultado)

def listar_usuarios():
    sql = "SELECT id, nome, cpf, email, tipo FROM usuarios"
    return consultar(sql)

def usuario_existe(id=None, email=None):
    sql = "SELECT * FROM usuarios WHERE id = ? OR email = ?"
    resultado = consultar(sql, (id, email))
    return bool(resultado)

def checar_senha(id=None, email=None, senha=None):
    sql = "SELECT * FROM usuarios WHERE (id = ? OR email = ?) AND senha = ?"
    resultado = consultar(sql, (id, email, senha))
    return bool(resultado)

def editar_usuario(id=None, email=None, senha=None, novo_nome=None, novo_email=None, nova_senha=None, novo_tipo=None):
    sql_busca = "SELECT * FROM usuarios WHERE id = ? OR email = ?"
    usuario = consultar(sql_busca, (id, email))
    if not usuario:
        return False, "Usuário não encontrado."

    if not checar_senha(id, email, senha):
        return False, "Senha incorreta."

    campos = []
    parametros = []

    if novo_nome:
        campos.append("nome = ?")
        parametros.append(novo_nome)
    if novo_email:
        campos.append("email = ?")
        parametros.append(novo_email)
    if nova_senha:
        campos.append("senha = ?")
        parametros.append(nova_senha)
    if novo_tipo:
        campos.append("tipo = ?")
        parametros.append(novo_tipo)

    if not campos:
        return True, "Nenhuma informação para atualizar."

    parametros.append(id if id else None)
    parametros.append(email if email else None)

    sql_update = f'''
        UPDATE usuarios
        SET {', '.join(campos)}
        WHERE id = ? OR email = ?
    '''

    executar_comando(sql_update, tuple(parametros))
    return True, "Usuário atualizado com sucesso!"

def deletar_usuario(id_ou_email):
    sql_verificar = "SELECT * FROM usuarios WHERE id = ? OR email = ?"
    usuario = consultar(sql_verificar, (id_ou_email, id_ou_email))
    if not usuario:
        return False, "Usuário não encontrado."

    executar_comando("DELETE FROM usuarios WHERE id = ? OR email = ?", (id_ou_email, id_ou_email))
    return True, "Usuário deletado com sucesso!"


# --- Funções interativas (inputs, prints, chamadas funções lógica) ---

def cadastrar_usuario_interativo():
    nome = input("Insira o nome do usuário: ")
    cpf = input("Insira o CPF do usuário (somente números): ")
    email = input("Insira o email do usuário: ")

    while True:
        tipo = input("Tipo de usuário ('cliente' ou 'funcionario'): ").lower()
        if tipo in ["cliente", "funcionario"]:
            break
        else:
            print("Tipo inválido. Digite 'cliente' ou 'funcionario'.")

    while True:
        senha = input("Insira a senha do usuário: ")
        senha_confirmada = input("Confirme a senha do usuário: ")
        if senha == senha_confirmada:
            break
        else:
            print("Senhas diferentes. Tente novamente.")

    sucesso, mensagem = registrar_usuario(nome, cpf, email, senha, tipo)
    print(mensagem)

def login_usuario_interativo():
    email = input("Insira seu email: ")
    senha = input("Insira sua senha: ")
    usuario = login_user(email, senha)

    if usuario:
        usuario_id, nome, tipo = usuario
        print(f"Login bem-sucedido! Bem-vindo(a), {nome} ({tipo})")
    else:
        print("Usuário ou senha inválidos!")

def listar_usuarios_interativo():
    usuarios = listar_usuarios()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for user in usuarios:
        print(f"ID: {user[0]} - Nome: {user[1]} - CPF: {user[2]} - Email: {user[3]} - Tipo: {user[4]}")

def editar_usuario_interativo():
    listar_usuarios_interativo()
    while True:
        id_ou_email = input("Insira o ID ou email do usuário que deseja editar: ")

        try:
            id_usuario = int(id_ou_email)
            email_usuario = None
        except ValueError:
            id_usuario = None
            email_usuario = id_ou_email

        if usuario_existe(id_usuario, email_usuario):
            break
        else:
            print("Usuário não encontrado. Tente novamente.")

    while True:
        senha = input("Confirme a senha do usuário para editar: ")
        if checar_senha(id_usuario, email_usuario, senha):
            break
        else:
            print("Senha incorreta. Tente novamente.")

    novo_nome = input("Novo nome (pressione Enter para manter o atual): ")
    novo_email = input("Novo email (pressione Enter para manter o atual): ")
    nova_senha = input("Nova senha (pressione Enter para manter a atual): ")
    novo_tipo = input("Novo tipo ('cliente' ou 'funcionario', pressione Enter para manter): ").lower()

    if novo_tipo not in ["cliente", "funcionario", ""]:
        print("Tipo inválido. O tipo não será alterado.")
        novo_tipo = None
    elif novo_tipo == "":
        novo_tipo = None

    sucesso, mensagem = editar_usuario(
        id=id_usuario,
        email=email_usuario,
        senha=senha,
        novo_nome=novo_nome if novo_nome.strip() != "" else None,
        novo_email=novo_email if novo_email.strip() != "" else None,
        nova_senha=nova_senha if nova_senha.strip() != "" else None,
        novo_tipo=novo_tipo
    )
    print(mensagem)

def deletar_usuario_interativo():
    listar_usuarios_interativo()
    id_ou_email = input("Insira o ID ou email do usuário que deseja excluir: ")
    sucesso, mensagem = deletar_usuario(id_ou_email)
    print(mensagem)

def login_user(email, senha):
    sql = "SELECT id, nome, tipo FROM usuarios WHERE email = ? AND senha = ?"
    resultado = consultar(sql, (email, senha))
    if resultado:
        return resultado[0]  # retorna (id, nome, tipo)
    return None
