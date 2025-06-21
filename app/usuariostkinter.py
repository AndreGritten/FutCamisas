import tkinter as tk
from tkinter import messagebox, ttk
from bancoDeDados.conexao import *
from usuarios import *

# Janela principal
janela = tk.Tk()
janela.title("FutCamisas - Gerenciamento de Usuários")
janela.geometry("600x500")
janela.config(bg="#121212")


# Função para cadastrar usuário
def cadastrar_usuario():
    def salvar():
        nome = entry_nome.get()
        cpf = entry_cpf.get()
        email = entry_email.get()
        senha = entry_senha.get()
        tipo = combo_tipo.get()

        if not (nome and cpf and email and senha and tipo):
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        try:
            register_user(nome, cpf, email, senha, tipo)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            cadastro.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    cadastro = tk.Toplevel(janela)
    cadastro.title("Cadastrar Usuário")
    cadastro.geometry("400x300")
    cadastro.config(bg="#1e1e1e")

    tk.Label(cadastro, text="Nome", bg="#1e1e1e", fg="white").pack()
    entry_nome = tk.Entry(cadastro)
    entry_nome.pack()

    tk.Label(cadastro, text="CPF", bg="#1e1e1e", fg="white").pack()
    entry_cpf = tk.Entry(cadastro)
    entry_cpf.pack()

    tk.Label(cadastro, text="Email", bg="#1e1e1e", fg="white").pack()
    entry_email = tk.Entry(cadastro)
    entry_email.pack()

    tk.Label(cadastro, text="Senha", bg="#1e1e1e", fg="white").pack()
    entry_senha = tk.Entry(cadastro, show="*")
    entry_senha.pack()

    tk.Label(cadastro, text="Tipo", bg="#1e1e1e", fg="white").pack()
    combo_tipo = ttk.Combobox(cadastro, values=["cliente", "funcionario"])
    combo_tipo.pack()

    tk.Button(cadastro, text="Cadastrar", command=salvar, bg="#00a86b", fg="white").pack(pady=10)


# Função para listar usuários
def listar_usuarios():
    lista = tk.Toplevel(janela)
    lista.title("Lista de Usuários")
    lista.geometry("600x400")
    lista.config(bg="#1e1e1e")

    tree = ttk.Treeview(lista, columns=("ID", "Nome", "CPF", "Email", "Tipo"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("CPF", text="CPF")
    tree.heading("Email", text="Email")
    tree.heading("Tipo", text="Tipo")

    tree.pack(fill=tk.BOTH, expand=True)

    usuarios = consultar("SELECT id, nome, cpf, email, tipo FROM usuarios")
    for user in usuarios:
        tree.insert("", tk.END, values=user)


# Função de login
def login_usuario():
    def autenticar():
        email = entry_email.get()
        senha = entry_senha.get()

        if login_user(email, senha):
            messagebox.showinfo("Login", "Login bem-sucedido!")
            login.destroy()
        else:
            messagebox.showerror("Erro", "Email ou senha inválidos!")

    login = tk.Toplevel(janela)
    login.title("Login de Usuário")
    login.geometry("300x200")
    login.config(bg="#1e1e1e")

    tk.Label(login, text="Email", bg="#1e1e1e", fg="white").pack()
    entry_email = tk.Entry(login)
    entry_email.pack()

    tk.Label(login, text="Senha", bg="#1e1e1e", fg="white").pack()
    entry_senha = tk.Entry(login, show="*")
    entry_senha.pack()

    tk.Button(login, text="Entrar", command=autenticar, bg="#007acc", fg="white").pack(pady=10)


# Botões principais
tk.Button(janela, text="Cadastrar Usuário", command=cadastrar_usuario, width=30, bg="#00a86b", fg="white").pack(pady=10)
tk.Button(janela, text="Listar Usuários", command=listar_usuarios, width=30, bg="#007acc", fg="white").pack(pady=10)
tk.Button(janela, text="Login de Usuário", command=login_usuario, width=30, bg="#f39c12", fg="white").pack(pady=10)
tk.Button(janela, text="Sair", command=janela.destroy, width=30, bg="#e74c3c", fg="white").pack(pady=20)

janela.mainloop()
