import sqlite3
import os
CAMINHO_BANCO = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'produtos.db')

def conectar():
  
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.execute("PRAGMA foreign_keys = ON;") 
    return conexao

def executar_comando(sql, parametros=()):
    
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(sql, parametros)
        conexao.commit()
    except sqlite3.Error as e:
        conexao.rollback()
        print(f"Erro SQLite ao executar comando: {e}")
        raise 
    finally:
        conexao.close()

def consultar(sql, parametros=()):
    
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(sql, parametros)
        resultados = cursor.fetchall()
        return resultados
    finally:
        conexao.close()

def executar_comando_com_retorno(sql, parametros=()):

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(sql, parametros)
    return cursor, conexao 
