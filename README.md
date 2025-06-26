# ⚽ FutCamisas: Sua Loja Online de Camisetas de Futebol!

Bem-vindo ao projeto **FutCamisas**, uma plataforma completa de e-commerce para a venda de camisetas de futebol, desenvolvida com uma arquitetura Full Stack. Este repositório contém todo o código-fonte necessário para rodar o sistema, que oferece desde a navegação pelo catálogo até a finalização de compras e um painel de administração para gestão.

---

## 🌟 Visão Geral do Projeto

O **FutCamisas** é um sistema web que simula uma loja virtual de camisas de times de futebol. Ele permite que usuários se cadastrem, naveguem por produtos, adicionem itens ao carrinho, finalizem compras e, no caso de funcionários, gerenciem produtos, usuários, estoque e visualizem relatórios de vendas.

---

## ✨ Principais Funcionalidades

- Autenticação de Usuários: Cadastro e login de clientes e funcionários.
- Catálogo de Produtos: Listagem de camisas com detalhes, preços e tamanhos disponíveis.
- Filtros e Busca: Encontre produtos por nome, time, preço e disponibilidade.
- Carrinho de Compras: Adicione, remova e ajuste a quantidade de itens antes da compra.
- Finalização de Compra: Processo seguro que registra a venda e atualiza o estoque.
- Relatórios de Vendas: Geração e visualização de logs detalhados.
- Painel Administrativo: Área restrita para gestão de usuários, produtos, vendas e estoque (CRUD completo).

---

## 🛠️ Tecnologias Utilizadas

### Frontend

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)

![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

### Backend

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![SQLite](https://img.shields.io/badge/SQLite-000?style=for-the-badge&logo=sqlite&logoColor=07405E)

---

## 🚀 Como Rodar o Projeto

### ✅ Pré-requisitos

- Python 3.x instalado no sistema.

### 1. Clonar o Repositório

```bash
git clone https://github.com/AndreGritten/FutCamisas.git
cd FutCamisas-3
```

### 2. Criar Ambiente Virtual (recomendado)

```bash
python -m venv .venv
```

Ative o ambiente virtual:

* Windows:

  ```bash
  .\.venv\Scripts\activate
  ```

* macOS/Linux:

  ```bash
  source ./.venv/bin/activate
  ```

### 3. Instalar Dependências

```bash
pip install Flask Flask-Cors
```

---

## 📁 Estrutura de Arquivos Essenciais

```
FutCamisas-3/
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── bancoDeDados/
│   │   ├── __init__.py
│   │   └── conexao.py
│   ├── estoque.py
│   ├── main.py
│   ├── produtos.py
│   ├── relatorios.py
│   ├── usuarios.py
│   └── vendas.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   ├── imagens/
│   │   ├── logo.png
│   │   ├── stadium_bg.jpg
│   │   ├── camisa_1.png
│   │   └── ...
├── produtos.db
├── relatorios_vendas.json
└── README.md
```
⚠️ Atenção: Crie o arquivo `relatorios_vendas.json` vazio na raiz do projeto, caso ele ainda não exista. Isso é necessário para que os relatórios de vendas funcionem corretamente.
---

## ▶️ Iniciar o Servidor Flask

Na raiz do projeto com o ambiente virtual ativado:

* Windows (PowerShell):

  ```powershell
  $env:FLASK_APP="app/app.py"
  ```

* Windows (CMD):

  ```cmd
  set FLASK_APP=app/app.py
  ```

* macOS/Linux:

  ```bash
  export FLASK_APP=app/app.py
  ```

Execute:

```bash
flask run
```

Acesse: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🔑 Credenciais de Acesso Iniciais

### Clientes

* [joao.silva@email.com](mailto:joao.silva@email.com) | senha123
* [maria.oliveira@email.com](mailto:maria.oliveira@email.com) | senha456

### Funcionários (Painel Admin)

* [carlos.pereira@email.com](mailto:carlos.pereira@email.com) | senha789
* [pedro.santos@email.com](mailto:pedro.santos@email.com) | senha654

---

## 🤝 Contribuição

Contribuições são bem-vindas! Abra uma *issue* ou envie um *pull request* com melhorias, correções ou sugestões.

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido com ⚽ e 💻 por FutCamisas**
