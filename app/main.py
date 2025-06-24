from produtos import *
from usuarios import *
from vendas import *
from estoque import *

def main():
    while True:
        print("\n==== FUTCAMISAS (Console) ====")
        print("1 - Login")
        print("2 - Cadastrar usuário")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            usuario_logado = login_usuario_interativo()
            if usuario_logado:
                usuario_id, nome, tipo, email, cpf = usuario_logado
                print(f"\nBem-vindo(a), {nome} ({tipo})!")
                if tipo == "cliente":
                    menu_cliente(usuario_logado)
                elif tipo == "funcionario":
                    menu_funcionario()
            else:
                print("Login inválido. Tente novamente.")
        elif opcao == "2":
            cadastrar_usuario_interativo()
        elif opcao == "0":
            print("Encerrando a aplicação de console...")
            break
        else:
            print("Opção inválida.")


def menu_funcionario():
    while True:
        print("\n=== MENU FUNCIONÁRIO ===")
        print("1 - Gerenciar Produtos")
        print("2 - Gerenciar Usuários")
        print("3 - Gerenciar Estoque")
        print("4 - Listar Todas as Vendas")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_produtos()
        elif opcao == "2":
            menu_usuarios()
        elif opcao == "3":
            menu_estoque()
        elif opcao == "4":
            listar_vendas_interativo()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def menu_cliente(usuario):
    usuario_id, nome, tipo, email, cpf = usuario
    while True:
        print("\n--- MENU CLIENTE ---")
        print("1 - Comprar produtos")
        print("2 - Ver minhas compras")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            realizar_venda_interativo(usuario)
        elif opcao == "2":
            buscar_historico_vendas_interativo(usuario_id)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_usuarios():
    while True:
        print("""\n===== MENU DE USUÁRIOS =====
1 - Cadastrar usuários
2 - Listar usuários
3 - Editar usuário
4 - Excluir usuário
0 - Sair""")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_usuario_interativo()

        elif opcao == "2":
            listar_usuarios_interativo()
        elif opcao == "3":
            editar_usuario_interativo()
        elif opcao == "4":
            deletar_usuario_interativo()
        elif opcao == "0":
            print("Saindo do menu de usuários...")
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

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_produto_interativo()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            editar_produto_interativo()
        elif opcao == "4":
            excluir_produto_interativo()
        elif opcao == "5":
            filtrar_produtos_por_nome(input("Digite o nome do time ou parte do nome para buscar: ").strip())
        elif opcao == "6":
            try:
                preco_min = float(input("Digite o preço mínimo: R$ "))
                preco_max = float(input("Digite o preço máximo: R$ "))
                filtrar_produtos_por_preco(preco_min, preco_max)
            except ValueError:
                print("Preço inválido.")
        elif opcao == "0":
            print("Saindo do menu de produtos...")
            break
        else:
            print("Opção inválida, tente novamente!")

def menu_estoque():
    while True:
        print("""\n===== MENU DO ESTOQUE =====
1 - Adicionar quantidade em estoque
2 - Consultar quantidade em estoque
0 - Sair""")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_quantidade_produto()
        elif opcao == "2":
            check_product_in_stock()
        elif opcao == "0":
            print("Saindo do menu de estoque...")
            break
        else:
            print("Opção inválida, tente novamente! ")

if __name__ == "__main__":
    main()