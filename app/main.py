from produtos import *
from usuarios import *
from vendas import *
from estoque import * 

def menu():
    while True:
        print("""\n===== FUTCAMISAS =====
1 - Usuários
2 - Estoque
3 - Vendas
4 - Produtos
0 - Sair""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_users()
        elif opcao == "2":
            menu_estoque()
        elif opcao == "3":
            menu_vendas()
        elif opcao == "4":
            menu_produtos()
        elif opcao == "0":
            print("Programa finalizado com sucesso! ")
            break
        else:
            print("Opção inválida, tente novamente! ")
    
            
def menu_users():
    while True:
        print("""\n===== MENU DE USUÁRIOS =====
1 - Cadastrar usuários
2 - Logar usuário
3 - Listar usuários
4 - Editar usuário
5 - Excluir usuário
0 - Sair""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
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

            register_user(nome, cpf, email, senha, tipo)

        elif opcao == "2":
            email = input("Insira seu email: ")
            senha = input("Insira sua senha: ")
            login_user(email, senha)

        elif opcao == "3":
            list_users()

        elif opcao == "4":
            list_users()

            while True:
                id_ou_email = input("Insira o ID ou email do usuário que deseja editar: ")

                try:
                    id_usuario = int(id_ou_email)
                    email_usuario = None
                except ValueError:
                    id_usuario = None
                    email_usuario = id_ou_email

                if user_exists(id_usuario, email_usuario):
                    break
                else:
                    print("Usuário não encontrado. Tente novamente.")

            while True:
                senha = input("Confirme a senha do usuário para editar: ")

                if check_password(id_usuario, email_usuario, senha):
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

            edit_user(
                id=id_usuario,
                email=email_usuario,
                password=senha,
                new_name=novo_nome if novo_nome.strip() != "" else None,
                new_email=novo_email if novo_email.strip() != "" else None,
                new_password=nova_senha if nova_senha.strip() != "" else None,
                new_tipo=novo_tipo
            )


        elif opcao == "5":
            list_users()
            id_ou_email = input("Insira o ID ou email do usuário que deseja excluir: ")
            delete_user(id_ou_email)

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente!")


def menu_produtos():
    while True:
        print("""\n===== MENU DE PRODUTOS =====
1 - Adicionar produto
2 - Listar produtos
3 - Editar produto
4 - Excluir produto
5 - Filtrar por nome
6 - Filtrar por preço
0 - Sair""")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome do produto: ")
            preco = float(input("Preço do produto: R$ "))

            tamanhos_dict = {}
            while True:
                tamanho = input("Informe um tamanho (ou Enter para finalizar): ").upper()
                if tamanho == "":
                    break
                quantidade = int(input(f"Quantidade para tamanho {tamanho}: "))
                if tamanho in tamanhos_dict:
                    tamanhos_dict[tamanho] += quantidade
                else:
                    tamanhos_dict[tamanho] = quantidade

            adicionar_produto(nome, preco, tamanhos_dict)

        elif opcao == "2":
            listar_produtos()

        elif opcao == "3":
            while True:
                listar_produtos()
                id_input = input("ID do produto para editar (ou pressione Enter para sair): ")
                if id_input.strip() == "":
                    break  # Sai do menu de edição
                try:
                    id_produto = int(id_input)
                except ValueError:
                    print("ID inválido. Digite um número válido.")
                    continue

                novo_nome = input("Novo nome (pressione Enter para manter o atual): ")
                novo_preco_input = input("Novo preço (pressione Enter para manter o atual): ")

                novo_tamanhos_dict = {}

                while True:
                    tamanho = input("Informe um tamanho (ou pressione Enter para finalizar tamanhos): ").upper()
                    if tamanho.strip() == "":
                        break
                    try:
                        quantidade = int(input(f"Quantidade para tamanho {tamanho}: "))
                    except ValueError:
                        print("Quantidade inválida. Informe um número inteiro.")
                        continue

                    if tamanho in novo_tamanhos_dict:
                        novo_tamanhos_dict[tamanho] += quantidade
                    else:
                        novo_tamanhos_dict[tamanho] = quantidade

                    # Pergunta se quer adicionar mais tamanhos
                    mais_tamanhos = input("Deseja adicionar mais quantidades para outro tamanho? (S/N): ").strip().upper()
                    if mais_tamanhos != "S":
                        break

                novo_preco = None
                if novo_preco_input.strip() != "":
                    try:
                        novo_preco = float(novo_preco_input)
                    except ValueError:
                        print("Preço inválido. Não foi alterado.")

                editar_produto(
                    id_produto,
                    novo_nome if novo_nome.strip() != "" else None,
                    novo_preco,
                    novo_tamanhos_dict if novo_tamanhos_dict else None
                )

                # Pergunta se deseja editar outro produto
                continuar = input("\nDeseja editar outro produto? (pressione Enter para sair ou qualquer tecla para continuar): ")
                if continuar.strip() == "":
                    break

        
        elif opcao == "4":
            try:
                id_produto = int(input("ID do produto para excluir: "))
            except ValueError:
                print("ID inválido.")
                continue

            excluir_produto(id_produto)

        elif opcao == "5":
            nome = input("Digite o nome do time ou parte do nome para buscar: ")
            filtrar_produtos_por_nome(nome)

        elif opcao == "6":
            try:
                preco_min = float(input("Digite o preço mínimo: R$ "))
                preco_max = float(input("Digite o preço máximo: R$ "))
                filtrar_produtos_por_preco(preco_min, preco_max)
            except ValueError:
                print("Preço inválido.")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente! ")

def menu_vendas():
    while True:
        print("""\n===== MENU DE VENDAS =====
1 - Realizar compra
2 - Listar vendas
3 - Listar compras do usuário
0 - Sair""")

        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            realizar_venda()

        elif opcao == "2":
            listar_vendas()

        elif opcao == "3":
            email = input("Digite seu email: ").strip()
            senha = input("Digite sua senha: ").strip()

            sql = "SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?"
            resultado = consultar(sql, (email, senha))

            if not resultado:
                print("Login inválido. Verifique email e senha.")
            else:
                usuario_id, nome = resultado[0]
                print(f"\nBem-vindo(a), {nome}!")
                buscar_historico_vendas(usuario_id)
        
        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente! ")

def menu_estoque():
    while True:
        print("""===== MENU DO ESTOQUE =====
1 - Adicionar quantidade em estoque 
2 - Consultar quantidade em estoque
0 - Sair""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_quantidade_produto() 
        
        elif opcao == "2":
            check_product_in_stock()
            
        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente! ")
        
    




if __name__ == "__main__":
    menu()