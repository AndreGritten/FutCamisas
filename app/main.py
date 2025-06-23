from produtos import *
from usuarios import *
from vendas import *
from estoque import * 

def main():
    while True:
        print("\n==== FUTCAMISAS ====")
        print("1 - Login")
        print("2 - Cadastrar usuário")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            email = input("Email: ").strip()
            senha = input("Senha: ").strip()
            usuario = login_user(email, senha)
            if usuario:
                usuario_id, nome, tipo = usuario
                print(f"\nBem-vindo(a), {nome}!")
                if tipo == "cliente":
                    menu_cliente(usuario)
                elif tipo == "funcionario":
                    menu_funcionario()
                else:
                    print("Tipo de usuário inválido.")
            else:
                print("Login inválido.")
        elif opcao == "2":
            cadastrar_usuario_interativo()
        elif opcao == "0":
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")


def menu_funcionario():
    while True:
        print("\n=== MENU FUNCIONÁRIO ===")
        print("1 - Adicionar produto")
        print("2 - Editar produto")
        print("3 - Excluir produto")
        print("4 - Adicionar quantidade ao estoque")
        print("5 - Listar produtos")
        print("6 - Listar todas as vendas")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_produto_interativo()
        elif opcao == "2":
            editar_produto_interativo()
        elif opcao == "3":
            excluir_produto_interativo()
        elif opcao == "4":
            adicionar_quantidade_produto()
        elif opcao == "5":
            listar_produtos()
        elif opcao == "6":
            listar_vendas_interativo()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def menu_cliente(usuario):
    while True:
        print("\n--- MENU CLIENTE ---")
        print("1 - Comprar produtos")
        print("2 - Ver minhas compras")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            realizar_venda_interativo(usuario)  # ou passar usuario_id, dependendo da sua função
        elif opcao == "2":
            listar_compras_usuario_interativo(usuario)  # já pede o login dentro, ou modifique para usar usuario_id direto
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

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
            cadastrar_usuario_interativo()
        elif opcao == "2":
            login_usuario_interativo()
        elif opcao == "3":
            listar_usuarios_interativo()
        elif opcao == "4":
            editar_usuario_interativo()
        elif opcao == "5":
            deletar_usuario_interativo()
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
            adicionar_produto_interativo()

        elif opcao == "2":
            listar_produtos()

        elif opcao == "3":
            editar_produto_interativo()

        elif opcao == "4":
            excluir_produto_interativo()

        elif opcao == "5":
            filtrar_produtos_por_nome_interativo()

        elif opcao == "6":
            filtrar_produtos_por_preco_interativo()

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente!")

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
    main()