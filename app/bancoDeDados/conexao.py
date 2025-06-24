# bancoDeDados/conexao.py

import sqlite3
import os

CAMINHO_BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'futCamisas.db')

def conectar():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON;")
    return conexao

# Novo: aceita uma conexão existente
def executar_comando(sql, parametros=(), conexao_existente=None):
    conexao = conexao_existente if conexao_existente else conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(sql, parametros)
        if not conexao_existente: # Somente commita e fecha se abriu a conexão
            conexao.commit()
    except sqlite3.Error as e:
        if not conexao_existente: # Somente faz rollback se abriu a conexão
            conexao.rollback()
        print(f"Erro SQLite ao executar comando: {e}")
        raise
    finally:
        if not conexao_existente: # Somente fecha se abriu a conexão
            conexao.close()

# Novo: aceita uma conexão existente
def consultar(sql, parametros=(), conexao_existente=None):
    conexao = conexao_existente if conexao_existente else conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(sql, parametros)
        resultados = cursor.fetchall()
        return resultados
    finally:
        if not conexao_existente: # Somente fecha se abriu a conexão
            conexao.close()

# Essa função já retorna a conexão para o chamador gerenciar
def executar_comando_com_retorno(sql, parametros=()):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(sql, parametros)
    return cursor, conexao