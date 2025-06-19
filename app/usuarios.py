from bancoDeDados.conexao import *
import sqlite3

def register_user(nome, cpf, email, senha, tipo):
    try:
        sql = '''
            INSERT INTO usuarios (nome, cpf, email, senha, tipo)
            VALUES (?, ?, ?, ?, ?)
        '''
        parametros = (nome, cpf, email, senha, tipo)
        executar_comando(sql, parametros)
        print(f"Usuário '{nome}' cadastrado com sucesso!")
    except sqlite3.IntegrityError as e:
        print(f"Erro ao cadastrar usuário: {e}")


def login_user(email, senha):
    sql = "SELECT * FROM usuarios WHERE email = ? AND senha = ?"
    resultado = consultar(sql, (email, senha))

    if resultado:
        print("Login bem-sucedido!")
        return True
    else:
        print("Usuário ou senha inválidos!")
        return False


def list_users():
    sql = "SELECT id, nome, cpf, email, tipo FROM usuarios"
    usuarios = consultar(sql)

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for user in usuarios:
        print(f"ID: {user[0]} - Nome: {user[1]} - CPF: {user[2]} - Email: {user[3]} - Tipo: {user[4]}")


def edit_user(id=None, email=None, password=None, new_name=None, new_email=None, new_password=None, new_tipo=None):
    sql_busca = "SELECT * FROM usuarios WHERE id = ? OR email = ?"
    usuario = consultar(sql_busca, (id, email))

    if not usuario:
        print("Usuário não encontrado.")
        return False

    sql_senha = "SELECT * FROM usuarios WHERE (id = ? OR email = ?) AND senha = ?"
    check = consultar(sql_senha, (id, email, password))
    if not check:
        print("Senha incorreta.")
        return False

    campos = []
    parametros = []

    if new_name:
        campos.append("nome = ?")
        parametros.append(new_name)
    if new_email:
        campos.append("email = ?")
        parametros.append(new_email)
    if new_password:
        campos.append("senha = ?")
        parametros.append(new_password)
    if new_tipo:
        campos.append("tipo = ?")
        parametros.append(new_tipo)

    if not campos:
        print("Nenhuma informação para atualizar.")
        return True  # Usuário encontrado, mas não quis alterar nada.

    parametros.append(id if id else None)
    parametros.append(email if email else None)

    sql_update = f'''
        UPDATE usuarios
        SET {', '.join(campos)}
        WHERE id = ? OR email = ?
    '''

    executar_comando(sql_update, tuple(parametros))
    print("Usuário atualizado com sucesso!")
    return True



def delete_user(id_or_email):
    sql_verificar = "SELECT * FROM usuarios WHERE id = ? OR email = ?"
    usuario = consultar(sql_verificar, (id_or_email, id_or_email))

    if not usuario:
        print("Usuário não encontrado.")
        return

    sql = "DELETE FROM usuarios WHERE id = ? OR email = ?"
    executar_comando(sql, (id_or_email, id_or_email))
    print("Usuário deletado com sucesso!")

def user_exists(id=None, email=None):
    sql = "SELECT * FROM usuarios WHERE id = ? OR email = ?"
    resultado = consultar(sql, (id, email))
    return bool(resultado)

def check_password(id=None, email=None, password=None):
    sql = "SELECT * FROM usuarios WHERE (id = ? OR email = ?) AND senha = ?"
    resultado = consultar(sql, (id, email, password))
    return bool(resultado)