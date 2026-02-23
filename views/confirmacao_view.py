# views/confirmacao_view.py
import discord
from ui.cores import Cores
from database.connection import SessionLocal
from models.usuario import Usuario
from models.jogador import Jogador
from data.faccao_config import FACCAO_INFO
from utils.faccao_utils import get_stats_faccao
from datetime import datetime
from views.select_faccao_view import mostrar_selecao_faccao  # Importa a função

class ConfirmacaoView(discord.ui.View):
    def __init__(self, user_id: int, faccao: str):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.faccao = faccao
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            embed = discord.Embed(
                description="❌ **Apenas quem iniciou pode interagir!**",
                color=Cores.VERMELHO_FORTE
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="✅ CONFIRMAR", style=discord.ButtonStyle.green)
    async def confirmar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.criar_personagem(interaction)
    
    @discord.ui.button(label="↩️ VOLTAR", style=discord.ButtonStyle.gray)
    async def voltar(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="⚔️ **Voltando...**", color=Cores.VERDE_CLARO)
        await interaction.response.edit_message(embed=embed, view=None)
        await mostrar_selecao_faccao(interaction)
    
    @discord.ui.button(label="❌ CANCELAR", style=discord.ButtonStyle.red)
    async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="⚜️ REGISTRO CANCELADO",
            description="Os mares continuarão te esperando... 👋",
            color=Cores.VERMELHO_FORTE
        )
        await interaction.response.edit_message(embed=embed, view=None)
    
    async def criar_personagem(self, interaction: discord.Interaction):
        db = SessionLocal()
        try:
            existe = db.query(Usuario).filter_by(discord_id=str(interaction.user.id)).first()
            if existe:
                embed = discord.Embed(
                    title="⚠️ AVENTURA JÁ INICIADA",
                    description="Você já possui um personagem!",
                    color=Cores.AMARELO
                )
                await interaction.response.edit_message(embed=embed, view=None)
                return
            
            novo_usuario = Usuario(
                discord_id=str(interaction.user.id),
                nome_discord=interaction.user.name,
                data_registro=datetime.now()
            )
            db.add(novo_usuario)
            db.flush()
            
            stats = get_stats_faccao(self.faccao)
            info = FACCAO_INFO[self.faccao]
            
            novo_jogador = Jogador(
                usuario_id=novo_usuario.id,
                faccao=self.faccao,
                nome_personagem=interaction.user.name,
                vida=stats.get("vida", 0),
                vida_max=stats.get("vida_max", stats.get("vida", 0)),
                armadura=stats.get("armadura", 0),
                velocidade=stats.get("velocidade", 0),
                berries=50
            )
            db.add(novo_jogador)
            db.commit()
            
            embed = discord.Embed(
                title="⚜️ BEM-VINDO!",
                description=f"Sua jornada como **{info['nome']}** começa AGORA!",
                color=info['cor']
            )
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed, view=None)
            
        except Exception as e:
            db.rollback()
            embed = discord.Embed(
                title="❌ ERRO",
                description=f"```{str(e)}```",
                color=Cores.VERMELHO_FORTE
            )
            await interaction.response.edit_message(embed=embed, view=None)
        finally:
            db.close()