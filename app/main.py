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

def menu_vendas():
    while True:
        print("""\n===== MENU DE VENDAS =====
1 - Realizar compra
2 - Listar vendas
3 - Listar compras do usuário
0 - Sair""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            realizar_venda_interativo()
        elif opcao == "2":
            listar_vendas_interativo()
        elif opcao == "3":
            listar_compras_usuario_interativo()
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
    menu()