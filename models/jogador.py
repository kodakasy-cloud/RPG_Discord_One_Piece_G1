from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class Jogador(Base):
    __tablename__ = 'jogadores'
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    nome = Column(String)
    nivel = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    berries = Column(Integer, default=0)
    
    # Atributos de combate
    vida = Column(Integer, default=10)
    vida_max = Column(Integer, default=10)
    energia = Column(Integer, default=10)
    energia_max = Column(Integer, default=10)
    armadura = Column(Integer, default=0)
    velocidade = Column(Integer, default=5)
    
    # Estilos de luta
    soco = Column(Integer, default=1)
    espada = Column(Integer, default=0)
    arma = Column(Integer, default=0)
    fruta = Column(Integer, default=0)
    
    # Hakis
    haki_armamento = Column(Integer, default=0)
    haki_observacao = Column(Integer, default=0)
    haki_rei = Column(Integer, default=0)
    
    # NOVOS CAMPOS - Raça e Sobrenome
    raca = Column(String, default=None, nullable=True)
    sobrenome = Column(String, default=None, nullable=True)
    
    faccao = Column(String, default="sem_faccao")
    vitorias = Column(Integer, default=0)
    derrotas = Column(Integer, default=0)
    
    usuario = relationship("Usuario", back_populates="jogador")