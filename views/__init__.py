# views/__init__.py
"""
Arquivo único com todas as views para evitar circular imports
"""
import discord
from ui.cores import Cores
from data.faccao_config import FACCAO_INFO
from utils.faccao_utils import get_stats_faccao
from database.connection import SessionLocal
from models.usuario import Usuario
from models.jogador import Jogador
from datetime import datetime

# =========== INICIAR VIEW ===========
class IniciarView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=120)
        self.user_id = user_id
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            embed = discord.Embed(
                description="❌ **Esta jornada não é sua!**",
                color=Cores.VERMELHO_FORTE
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="🌟 INICIAR JORNADA", style=discord.ButtonStyle.blurple, emoji="⚔️")
    async def iniciar(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        embed = discord.Embed(
            description="⚔️ **Preparando sua aventura...**",
            color=Cores.VERDE_CLARO
        )
        await interaction.response.edit_message(embed=embed, view=self)
        await mostrar_selecao_faccao(interaction)


# =========== SELEÇÃO DE FACÇÃO ===========
class FaccaoSelect(discord.ui.Select):
    def __init__(self, user_id: int):
        self.user_id = user_id
        options = []
        
        for key, info in FACCAO_INFO.items():
            stats = get_stats_faccao(key)
            options.append(
                discord.SelectOption(
                    label=info['nome'],
                    description=f"❤️ {stats.get('vida', 0)} | 🛡️ {stats.get('armadura', 0)} | ⚡ {stats.get('velocidade', 0)}",
                    emoji=info['emoji'],
                    value=key
                )
            )
        
        super().__init__(
            placeholder="⚔️ Escolha sua facção...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Apenas quem iniciou pode escolher!", ephemeral=True)
            return
        
        await mostrar_detalhes_faccao(interaction, self.values[0])


class FaccaoSelectView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.add_item(FaccaoSelect(user_id))


async def mostrar_detalhes_faccao(interaction: discord.Interaction, faccao: str):
    info = FACCAO_INFO[faccao]
    stats = get_stats_faccao(faccao)
    
    embed = discord.Embed(
        title=f"{info['emoji']} {info['nome']}",
        description=f"*{info['descricao']}*",
        color=info['cor']
    )
    
    embed.add_field(name="📖 História", value=info['historia'][:100] + "...", inline=False)
    
    status = (
        f"❤️ Vida: {stats.get('vida', 0)}/{stats.get('vida_max', stats.get('vida', 0))}\n"
        f"🛡️ Armadura: {stats.get('armadura', 0)}\n"
        f"⚡ Velocidade: {stats.get('velocidade', 0)}"
    )
    embed.add_field(name="📊 Status", value=status, inline=True)
    embed.add_field(name="⚔️ Estilo", value=info['estilo'], inline=True)
    embed.add_field(name="✨ Destaque", value=info['destaque'], inline=True)
    
    embed.set_footer(text="Esta será sua jornada. Deseja prosseguir?")
    
    view = ConfirmacaoView(interaction.user.id, faccao)
    await interaction.response.edit_message(embed=embed, view=view)


async def mostrar_selecao_faccao(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚔️ ESCOLHA SEU DESTINO",
        description="**Quatro caminhos te aguardam. Qual será sua jornada?**\n",
        color=Cores.AZUL_FORTE
    )
    
    faccoes_text = ""
    for key, info in FACCAO_INFO.items():
        stats = get_stats_faccao(key)
        faccoes_text += (
            f"{info['emoji']} **{info['nome']}**\n"
            f"┗ ❤️ {stats.get('vida', 0)} | 🛡️ {stats.get('armadura', 0)} | ⚡ {stats.get('velocidade', 0)}\n"
            f"┗ *{info['estilo']}*\n\n"
        )
    
    embed.add_field(name="Facções", value=faccoes_text, inline=False)
    embed.set_footer(text="Selecione uma facção no menu abaixo para ver detalhes")
    
    view = FaccaoSelectView(interaction.user.id)
    await interaction.edit_original_response(embed=embed, view=view)


# =========== CONFIRMAÇÃO ===========
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


# =========== EXPORTAÇÕES ===========
__all__ = [
    'IniciarView',
    'FaccaoSelectView',
    'ConfirmacaoView',
    'mostrar_selecao_faccao'
]