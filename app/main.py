# app/main.py

from produtos import adicionar_produto, listar_produtos, editar_produto, excluir_produto

# Simulação simples
def menu():
    while True:
            print("\n===== MENU DE PRODUTOS =====")
            print("1 - Adicionar produto")
            print("2 - Listar produtos")
            print("3 - Editar produto")
            print("4 - Excluir produto")
            print("0 - Sair")

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

if __name__ == "__main__":
    menu()