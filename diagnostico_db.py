# diagnostico_db.py
import sqlite3
import os
from pathlib import Path

print("="*50)
print("DIAGNÓSTICO DO BANCO DE DADOS")
print("="*50)

# 1. Localizar o arquivo do banco
caminho_db = Path("OP_database.db")
print(f"\n Procurando banco em: {caminho_db.absolute()}")

if not caminho_db.exists():
    print(" Arquivo do banco NÃO encontrado!")
    # Procura por outros arquivos .db
    outros_dbs = list(Path(".").glob("*.db"))
    if outros_dbs:
        print(f" Outros bancos encontrados: {[db.name for db in outros_dbs]}")
else:
    print(f" Arquivo encontrado! Tamanho: {caminho_db.stat().st_size} bytes")

    # 2. Conectar e listar tabelas
    print("\n Tabelas no banco (SQLite nativo):")
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    
    if not tabelas:
        print("   Nenhuma tabela encontrada.")
    else:
        for tabela in tabelas:
            nome_tabela = tabela[0]
            print(f"   - {nome_tabela}")
            # Mostrar colunas da tabela 'usuarios' se ela existir
            if nome_tabela == 'usuarios':
                cursor.execute(f"PRAGMA table_info(usuarios)")
                colunas = cursor.fetchall()
                print(f"     Colunas em 'usuarios':")
                for col in colunas:
                    print(f"       • {col[1]} ({col[2]})")
    conn.close()

print("\n" + "="*50)