import tkinter as tk
from tkinter import ttk, messagebox

from usuariostkinter import *
from produtos import *
from vendas import *
from estoque import *

# Funções dos botões
def abrir_menu_usuarios():
    janela_usuarios = tk.Toplevel(root)
    janela_usuarios.title("Menu de Usuários")
    janela_usuarios.geometry("400x400")

    ttk.Label(janela_usuarios, text="Menu de Usuários", font=("Arial", 16, "bold")).pack(pady=10)

    botoes = [
        ("Cadastrar Usuário", lambda: messagebox.showinfo("Em desenvolvimento", "Funcionalidade de cadastro.")),
        ("Listar Usuários", list_users),
        ("Editar Usuário", lambda: messagebox.showinfo("Em desenvolvimento", "Funcionalidade de edição.")),
        ("Excluir Usuário", lambda: messagebox.showinfo("Em desenvolvimento", "Funcionalidade de exclusão.")),
    ]

    for texto, comando in botoes:
        ttk.Button(janela_usuarios, text=texto, command=comando).pack(pady=5, fill="x")


def abrir_menu_produtos():
    janela_produtos = tk.Toplevel(root)
    janela_produtos.title("Menu de Produtos")
    janela_produtos.geometry("400x400")

    ttk.Label(janela_produtos, text="Menu de Produtos", font=("Arial", 16, "bold")).pack(pady=10)

    botoes = [
        ("Adicionar Produto", lambda: messagebox.showinfo("Em desenvolvimento", "Funcionalidade de adicionar.")),
        ("Listar Produtos", listar_produtos),
        ("Editar Produto", lambda: messagebox.showinfo("Em desenvolvimento", "Funcionalidade de edição.")),
        ("Excluir Produto", lambda: messagebox.showinfo("Em desenvolvimento", "Funcionalidade de exclusão.")),
    ]

    for texto, comando in botoes:
        ttk.Button(janela_produtos, text=texto, command=comando).pack(pady=5, fill="x")


def abrir_menu_vendas():
    janela_vendas = tk.Toplevel(root)
    janela_vendas.title("Menu de Vendas")
    janela_vendas.geometry("400x400")

    ttk.Label(janela_vendas, text="Menu de Vendas", font=("Arial", 16, "bold")).pack(pady=10)

    botoes = [
        ("Realizar Compra", realizar_venda),
        ("Listar Vendas", listar_vendas),
        ("Histórico de Compras", lambda: messagebox.showinfo("Em desenvolvimento", "Funcionalidade de histórico.")),
    ]

    for texto, comando in botoes:
        ttk.Button(janela_vendas, text=texto, command=comando).pack(pady=5, fill="x")


def abrir_menu_estoque():
    janela_estoque = tk.Toplevel(root)
    janela_estoque.title("Menu de Estoque")
    janela_estoque.geometry("400x400")

    ttk.Label(janela_estoque, text="Menu de Estoque", font=("Arial", 16, "bold")).pack(pady=10)

    botoes = [
        ("Adicionar ao Estoque", adicionar_quantidade_produto),
        ("Consultar Estoque", check_product_in_stock),
    ]

    for texto, comando in botoes:
        ttk.Button(janela_estoque, text=texto, command=comando).pack(pady=5, fill="x")


# Janela Principal
root = tk.Tk()
root.title("FutCamisas - Loja de Futebol")
root.geometry("500x500")
root.configure(bg="#1c1c1c")

# Estilo moderno
style = ttk.Style(root)
style.theme_use("default")
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", foreground="white", background="#1c1c1c")

ttk.Label(root, text="FutCamisas", font=("Arial", 24, "bold")).pack(pady=20)
ttk.Label(root, text="Escolha uma opção", font=("Arial", 14)).pack(pady=5)

# Botões principais
botoes_principais = [
    ("Usuários", abrir_menu_usuarios),
    ("Produtos", abrir_menu_produtos),
    ("Vendas", abrir_menu_vendas),
    ("Estoque", abrir_menu_estoque),
    ("Sair", root.destroy),
]

for texto, comando in botoes_principais:
    ttk.Button(root, text=texto, command=comando).pack(pady=8, ipadx=10, fill="x", padx=60)

root.mainloop()
