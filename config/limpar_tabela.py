# reset_simples.py
"""
Versão simplificada - só apaga e recria sem perguntas
"""

import os
from database.connection import engine, Base
from models.usuario import Usuario
from models.jogador import Jogador

print("="*50)
print(" RESETANDO BANCO DE DADOS")
print("="*50)

# Apaga o banco antigo
db_file = "OP_database.db"
if os.path.exists(db_file):
    os.remove(db_file)
    print(f" Banco antigo removido: {db_file}")

# Cria novo banco com todas as tabelas
print("\n Criando novas tabelas...")
Base.metadata.create_all(bind=engine)
print(" Tabelas recriadas com sucesso!")

# Verifica
import sqlite3
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("\n Tabelas criadas:")
for tabela in tabelas:
    print(f"  - {tabela[0]}")
conn.close()

print("\n" + "="*50)
print(" Banco pronto para uso!")
print("="*50)