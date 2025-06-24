import sqlite3

from .bancoDeDados.conexao import executar_comando, consultar, conectar


def register_user(nome, email, senha, cpf, tipo='cliente'):
    try:
        if consultar("SELECT id FROM usuarios WHERE email = ?", (email,)):
            return False, "Email já cadastrado."
        if consultar("SELECT id FROM usuarios WHERE cpf = ?", (cpf,)):
            return False, "CPF já cadastrado."

        sql = '''
            INSERT INTO usuarios (nome, email, senha, cpf, tipo)
            VALUES (?, ?, ?, ?, ?)
        '''
        executar_comando(sql, (nome, email, senha, cpf, tipo))
        return True, f"Usuário '{nome}' cadastrado com sucesso!"
    except sqlite3.Error as e:
        return False, f"Erro ao cadastrar usuário: {e}"

def login_user(email, senha):
    sql = "SELECT id, nome, tipo, cpf FROM usuarios WHERE email = ? AND senha = ?"
    resultado = consultar(sql, (email, senha))
    if resultado:
        user_data = resultado[0]
        return True, "Login bem-sucedido!", user_data
    return False, "Email ou senha inválidos!", None

def edit_user(id=None, email=None, password=None, new_name=None, new_email=None, new_password=None, new_tipo=None):
    sql_busca = "SELECT id, email, senha FROM usuarios WHERE id = ? OR email = ?"
    usuario_existente = consultar(sql_busca, (id, email))

    if not usuario_existente:
        return False, "Usuário não encontrado."

    user_id_db, user_email_db, user_senha_db = usuario_existente[0]

    if user_senha_db != password:
        return False, "Senha incorreta para edição."

    campos_update = []
    parametros = []

    if new_name:
        campos_update.append("nome = ?")
        parametros.append(new_name)
    if new_email:
        if consultar("SELECT id FROM usuarios WHERE email = ? AND id != ?", (new_email, user_id_db)):
            return False, "Novo email já está em uso por outro usuário."
        campos_update.append("email = ?")
        parametros.append(new_email)
    if new_password:
        campos_update.append("senha = ?")
        parametros.append(new_password)
    if new_tipo and new_tipo in ['cliente', 'funcionario']:
        campos_update.append("tipo = ?")
        parametros.append(new_tipo)

    if not campos_update:
        return True, "Nenhuma informação para atualizar."

    sql_update = f'''
        UPDATE usuarios
        SET {', '.join(campos_update)}
        WHERE id = ?
    '''
    parametros.append(user_id_db)

    try:
        executar_comando(sql_update, tuple(parametros))
        return True, "Usuário atualizado com sucesso!"
    except sqlite3.Error as e:
        return False, f"Erro ao atualizar usuário: {e}"

def delete_user(id_or_email, password=None):
    sql_verificar = "SELECT id, senha FROM usuarios WHERE id = ? OR email = ?"
    usuario_existente = consultar(sql_verificar, (id_or_email, id_or_email))

    if not usuario_existente:
        return False, "Usuário não encontrado."

    user_id_db, user_senha_db = usuario_existente[0]

    if password and user_senha_db != password:
        return False, "Senha de confirmação incorreta."

    sql_delete = "DELETE FROM usuarios WHERE id = ?"
    try:
        executar_comando(sql_delete, (user_id_db,))
        return True, "Usuário deletado com sucesso!"
    except sqlite3.Error as e:
        return False, f"Erro ao deletar usuário: {e}"


def list_users():
    sql = "SELECT id, nome, cpf, email, tipo FROM usuarios"
    return consultar(sql)

def cadastrar_usuario_interativo():
    nome = input("Insira o nome do usuário: ")
    cpf = input("Insira o CPF do usuário (somente números): ")
    email = input("Insira o email do usuário: ")

    while True:
        tipo = input("Tipo de usuário ('cliente' ou 'funcionario'): ").lower().strip()
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

    sucesso, mensagem = register_user(nome, email, senha, cpf, tipo)
    print(mensagem)

def login_usuario_interativo():
    email = input("Insira seu email: ").strip()
    senha = input("Insira sua senha: ").strip()
    sucesso, mensagem, user_data = login_user(email, senha)

    if sucesso:
        print(f"Login bem-sucedido! Bem-vindo(a), {user_data[1]} ({user_data[2]})")
        return user_data
    else:
        print(mensagem)
        return None

def listar_usuarios_interativo():
    usuarios = list_users()
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for user in usuarios:
        print(f"ID: {user[0]} - Nome: {user[1]} - CPF: {user[2]} - Email: {user[3]} - Tipo: {user[4]}")

def editar_usuario_interativo():
    listar_usuarios_interativos()
    while True:
        id_ou_email = input("Insira o ID ou email do usuário que deseja editar: ").strip()
        if not id_ou_email:
            print("Operação cancelada.")
            return

        try:
            id_usuario = int(id_ou_email)
            email_usuario = None
        except ValueError:
            id_usuario = None
            email_usuario = id_ou_email

        sql_verificar = "SELECT id FROM usuarios WHERE id = ? OR email = ?"
        if consultar(sql_verificar, (id_usuario, email_usuario)):
            break
        else:
            print("Usuário não encontrado. Tente novamente.")

    while True:
        senha = input("Confirme a senha do usuário para editar: ").strip()
        sql_checar_senha = "SELECT id FROM usuarios WHERE (id = ? OR email = ?) AND senha = ?"
        if consultar(sql_checar_senha, (id_usuario, email_usuario, senha)):
            break
        else:
            print("Senha incorreta. Tente novamente.")

    novo_nome = input("Novo nome (pressione Enter para manter o atual): ").strip()
    novo_email = input("Novo email (pressione Enter para manter o atual): ").strip()
    nova_senha = input("Nova senha (pressione Enter para manter a atual): ").strip()
    novo_tipo = input("Novo tipo ('cliente' ou 'funcionario', pressione Enter para manter): ").lower().strip()

    if novo_tipo not in ["cliente", "funcionario", ""]:
        print("Tipo inválido. O tipo não será alterado.")
        novo_tipo = None
    elif novo_tipo == "":
        novo_tipo = None

    sucesso, mensagem = edit_user(
        id=id_usuario,
        email=email_usuario,
        password=senha,
        new_name=novo_nome if novo_nome != "" else None,
        new_email=novo_email if novo_email != "" else None,
        new_password=nova_senha if nova_senha != "" else None,
        new_tipo=novo_tipo
    )
    print(mensagem)

def deletar_usuario_interativo():
    listar_usuarios_interativos()
    id_ou_email = input("Insira o ID ou email do usuário que deseja excluir: ").strip()
    if not id_ou_email:
        print("Operação cancelada.")
        return

    senha = input("Confirme a senha do usuário para exclusão: ").strip()

    sucesso, mensagem = delete_user(id_ou_email, password=senha)
    print(mensagem)