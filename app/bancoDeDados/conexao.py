import sqlite3
import os

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), 'futCamisas.db')

def conectar():
    return sqlite3.connect(CAMINHO_BANCO)

def executar_comando(sql, parametros=()):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(sql, parametros)
    conexao.commit()
    conexao.close()

def consultar(sql, parametros=()):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(sql, parametros)
    resultados = cursor.fetchall()
    conexao.close()
    return resultados
