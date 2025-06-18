from produtos import *
from usuarios import *
from vendas import *
from estoque import * 

def menu():
    while True:
        print("""===== FUTCAMISAS =====
1 - Usuários
2 - Produtos
3 - Vendas
4 - Estoque
0 - Sair""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_users()
        elif opcao == "2":
            menu_produtos()
        elif opcao == "3":
            menu_vendas()
        elif opcao == "4":
            menu_estoque()
        elif opcao == "0":
            print("Programa finalizado com sucesso! ")
            break
        else:
            print("Opção inválida, tente novamente! ")
    
            
def menu_users():
    while True:
        print("""===== MENU DE USUÁRIOS =====
1 - Cadastrar usuários
2 - Logar usuário
3 - Listar usuários
4 - Editar usuário
5 - Excluir usuário
0 - Sair""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
           nome = input("Insira o nome do usuário: ")
           email = input("Insira o email do usuário: ")
           while True:
               senha = input("Insira a senha do usuário: ")
               senha_confirmada = input("Confirme a senha do usuário: ")
               if senha == senha_confirmada:
                   break
               else:
                   print("Senhas diferentes, por favor confirme a senha do usuário! ")
           register_user(nome, email, senha)

        elif opcao == "2":
            email = input("Insira seu email: ")
            senha = input("Insira sua senha: ")
            login_user(email, senha)

        elif opcao == "3":
            list_users()

        elif opcao == "4":
            list_users()
            id_ou_email = input("Insira o ID ou email do usuário que deseja editar: ")

            try:
                id_usuario = int(id_ou_email)
                email_usuario = None
            except ValueError:
                id_usuario = None
                email_usuario = id_ou_email

            senha = input("Confirme a senha do usuário: ")

            novo_nome = input("Novo nome (pressione Enter para manter o atual): ")
            novo_email = input("Novo email (pressione Enter para manter o atual): ")
            nova_senha = input("Nova senha (pressione Enter para manter a atual): ")

            edit_user(
                id=id_usuario,
                email=email_usuario,
                password=senha,
                new_name=novo_nome if novo_nome.strip() != "" else None,
                new_email=novo_email if novo_email.strip() != "" else None,
                new_password=nova_senha if nova_senha.strip() != "" else None
            )


        elif opcao == "5":
            list_users()
            id_ou_email = input("Insira o ID ou email do usuário que deseja excluir: ")
            delete_user(id_ou_email)

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente! ")
    

def menu_produtos():
    while True:
        print("""===== MENU DE PRODUTOS =====
1 - Adicionar produto
2 - Listar produtos
3 - Editar produto
4 - Excluir produto
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
            listar_produtos()                
            id_produto = int(input("ID do produto para editar: "))
            novo_nome = input("Novo nome (pressione Enter para manter o atual): ")
            novo_preco_input = input("Novo preço (pressione Enter para manter o atual): ")
            novo_tamanhos_dict = {}
            while True:
                tamanho = input("Informe um tamanho (ou Enter para finalizar): ").upper()
                if tamanho == "":
                    break
                quantidade = int(input(f"Quantidade para tamanho {tamanho}: "))
                if tamanho in novo_tamanhos_dict:
                    novo_tamanhos_dict[tamanho] += quantidade
                else:
                    novo_tamanhos_dict[tamanho] = quantidade
        
            novo_preco = None
            if novo_preco_input.strip() != "":
                novo_preco = float(novo_preco_input)
        
            editar_produto(
                id_produto, 
                novo_nome if novo_nome.strip() != "" else None,
                novo_preco,
                novo_tamanhos_dict if novo_tamanhos_dict else None
            )   
        
        elif opcao == "4":
            id_produto = int(input("ID do produto para excluir: "))
            excluir_produto(id_produto)

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente! ")


def menu_vendas():
    while True:
        print("""===== MENU DE VENDAS =====
1 - Registrar venda 
2 - Atualizar estoque
0 - Sair""")

        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            register_sale()

        elif opcao == "2":
            update_stock()
        
        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente! ")



def menu_estoque():
    while True:
        print("""===== MENU DO ESTOQUE =====
1 - Adicionar qtd de um produto ao estoque 
2 - Consultar qtd em estoque
0 - Sair""")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            add_product_to_stock()  
        
        elif opcao == "2":
            check_product_in_stock()
            
        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente! ")
        
    




if __name__ == "__main__":
    menu()