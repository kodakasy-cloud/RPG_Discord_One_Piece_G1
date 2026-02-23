# views/confirmacao_view.py
import discord
import asyncio
from ui.cores import Cores
from database.connection import SessionLocal
from models.usuario import Usuario
from models.jogador import Jogador
from data.faccao_config import FACCAO_INFO
from utils.faccao_utils import get_stats_faccao
from datetime import datetime
from views.select_faccao_view import mostrar_selecao_faccao

class ConfirmacaoView(discord.ui.View):
    def __init__(self, user_id: int, faccao: str, bot):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.faccao = faccao
        self.bot = bot 
    
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
        """Cria o personagem no banco de dados com contagem regressiva"""
        
        db = SessionLocal()
        try:
            # Verifica se já existe
            existe = db.query(Usuario).filter_by(discord_id=str(interaction.user.id)).first()
            if existe:
                embed = discord.Embed(
                    title="⚠️ AVENTURA JÁ INICIADA",
                    description="Você já possui um personagem!",
                    color=Cores.AMARELO
                )
                await interaction.response.edit_message(embed=embed, view=None)
                return
            
            # Cria usuário
            novo_usuario = Usuario(
                discord_id=str(interaction.user.id),
                nome_discord=interaction.user.name,
                data_registro=datetime.now()
            )
            db.add(novo_usuario)
            db.flush()
            
            # Pega stats da facção
            stats = get_stats_faccao(self.faccao)
            info = FACCAO_INFO[self.faccao]
            
            # Cria jogador
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
            
            # =========== CONTAGEM REGRESSIVA ===========
            
            # Mensagem de sucesso inicial
            embed = discord.Embed(
                title=f"{info['emoji']} BEM-VINDO!",
                description=f"Está preparado para todos os desafios?",
                color=info['cor']
            )
            embed.set_thumbnail(url=interaction.user.display_avatar.url)
            await interaction.response.edit_message(embed=embed, view=None)
            
            # Contagem regressiva (3 mensagens)
            await asyncio.sleep(1.5)
            
            for i in range(3, 0, -1):
                embed = discord.Embed(
                    description=f"⚔️ **Sua aventura irá começar em {i}...**",
                    color=Cores.DOURADO
                )
                await interaction.edit_original_response(embed=embed)
                await asyncio.sleep(1)
            
            # =========== REDIRECIONA PARA O PERFIL ===========
            
            # Cria um contexto falso para chamar o comando perfil
            ctx = await self.bot.get_context(interaction.message)
            ctx.author = interaction.user
            ctx.command = self.bot.get_command("perfil")
            
            if ctx.command:
                await self.bot.get_cog("PerfilCog").perfil(ctx)
            else:
                # Fallback: mostra o perfil manualmente
                await self.mostrar_perfil_direto(interaction, novo_jogador, info)
                
        except Exception as e:
            db.rollback()
            embed = discord.Embed(
                title="❌ ERRO",
                description=f"```{str(e)}```",
                color=Cores.VERMELHO_FORTE
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        finally:
            db.close()

    async def mostrar_perfil_direto(self, interaction: discord.Interaction, jogador, info):
        """Mostra o perfil diretamente (fallback)"""
        embed = discord.Embed(
            title=f"⚔️ PERFIL DE {interaction.user.name.upper()} ⚔️",
            color=info['cor']
        )
        
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        info_basica = (
            f"**Facção:** {info['emoji']} {info['nome']}\n"
            f"**Nível:** {jogador.nivel}\n"
            f"**Berries:** 💰 {jogador.berries}"
        )
        embed.add_field(name="📋 INFORMAÇÕES", value=info_basica, inline=False)
        
        status = (
            f"❤️ **Vida:** {jogador.vida}/{jogador.vida_max}\n"
            f"🛡️ **Armadura:** {jogador.armadura}\n"
            f"⚡ **Velocidade:** {jogador.velocidade}"
        )
        embed.add_field(name="⚔️ COMBATE", value=status, inline=True)
        
        await interaction.followup.send(embed=embed)