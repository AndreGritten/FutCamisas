users = []


def register_user(name, email, password):
    user = {
        "id": len(users) + 1,
        "name": name,
        "email": email,
        "password": password    
    }
    users.append(user)
    print(f"{name} cadastrado com sucesso!")


def login_user(email, password):
    for user in users:
        if user["email"] ==  email and user["password"] == password:
            print("Login bem sucedido! ")
            return
    print("Usuário ou senha inválidos! ")


def edit_user(id, email,password, new_name=None, new_email=None, new_password=None):
    for user in users:
        if user["id"] == id or user["email"] == email:
            if new_name:
                user["name"] = new_name

            if new_email:
                if user["password"] == password:
                    user["email"] = new_email
                else:
                    print("Senha inválida! ")
                    return

            if new_password:
                if user["password"] == password:
                    user["password"] = new_password
                else:
                    print("Senha inválida! ")
                    return
            
            print("Usuário atualizado com sucesso! ")
            return
        
    print("Usuário não encontrado")


def delete_user(id_or_email):
    global users
    for i, user in enumerate(users):
        if user["id"] == id_or_email or user["email"] == id_or_email:
            del users[i]
            print("Usuário deletado com sucesso! ")
    print("Usuário não encontrado! ")


def list_users():
    if not users:
        print("Nenhum usuário cadastrado! ")
    for user in users:
        print(f"ID: {user["id"]} - Nome: {user["name"]} - Email: {user["email"]}")