# criar_tabelas.py
from database.connection import engine, Base
from models.usuario import Usuario
from models.jogador import Jogador

print("="*50)
print(" FORÇANDO CRIAÇÃO DAS TABELAS")
print("="*50)

# Mostra quais tabelas serão criadas
print("\n Modelos registrados no SQLAlchemy:")
print(f"   - {Usuario.__tablename__}")
print(f"   - {Jogador.__tablename__}")

# Cria as tabelas
print("\n  Executando Base.metadata.create_all...")
Base.metadata.create_all(bind=engine)
print(" Comando executado!")

# Verifica se as tabelas foram criadas
import sqlite3
conn = sqlite3.connect('OP_database.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()

print("\n Tabelas encontradas no banco:")
if tabelas:
    for tabela in tabelas:
        print(f"   - {tabela[0]}")
else:
    print("    NENHUMA tabela encontrada!")

conn.close()
print("\n" + "="*50)