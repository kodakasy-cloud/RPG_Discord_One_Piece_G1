# models/usuario.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database.connection import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    discord_id = Column(String, unique=True, nullable=False)
    nome_discord = Column(String, nullable=False)
    data_registro = Column(DateTime, default=datetime.now)
    
    # Relacionamento com Jogador
    jogador = relationship("Jogador", back_populates="usuario", uselist=False)
    
    def __repr__(self):
        return f"<Usuario {self.nome_discord}>"