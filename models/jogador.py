# models/jogador.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class Jogador(Base):
    __tablename__ = 'jogadores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), unique=True, nullable=False)
    
    # Informações básicas
    faccao = Column(String, nullable=False)
    nome_personagem = Column(String, nullable=False)
    
    # Atributos principais
    vida = Column(Integer, default=10)
    vida_max = Column(Integer, default=10)
    energia = Column(Integer, default=2)
    energia_max = Column(Integer, default=2)
    armadura = Column(Integer, default=0)
    velocidade = Column(Integer, default=4)
    
    # Estilos de luta
    soco = Column(Integer, default=1)
    espada = Column(Integer, default=0)
    arma = Column(Integer, default=0)
    fruta = Column(Integer, default=0)
    
    # Hakis
    haki_armamento = Column(Integer, default=0)
    haki_observacao = Column(Integer, default=0)
    haki_rei = Column(Integer, default=0)
    
    # Progressão
    nivel = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    berries = Column(Integer, default=50)
    vitorias = Column(Integer, default=0)
    derrotas = Column(Integer, default=0)
    
    # Relacionamento com Usuario
    usuario = relationship("Usuario", back_populates="jogador")
    
    def __repr__(self):
        return f"<Jogador {self.nome_personagem} - Nv.{self.nivel}>"