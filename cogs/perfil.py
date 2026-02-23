# cogs/perfil.py
import discord
from discord.ext import commands
from discord import app_commands
from database.connection import SessionLocal
from models.usuario import Usuario
from models.jogador import Jogador
from data.faccao_config import FACCAO_INFO
from utils.faccao_utils import get_stats_faccao
from ui.cores import Cores
from datetime import datetime
from views.perfil_menu_view import PerfilMenuView

class PerfilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="perfil", aliases=["profile", "status", "stats"])
    async def perfil(self, ctx, membro: discord.Member = None):
        """Veja o perfil de um jogador com menu interativo"""
        
        # Se não mencionar ninguém, mostra o próprio perfil
        if membro is None:
            membro = ctx.author
        
        db = SessionLocal()
        try:
            # Busca o usuário no banco
            usuario = db.query(Usuario).filter_by(
                discord_id=str(membro.id)
            ).first()
            
            if not usuario:
                if membro == ctx.author:
                    await ctx.send("❌ Você ainda não tem um personagem! Use `!registrar` para criar um.")
                else:
                    await ctx.send(f"❌ {membro.name} ainda não tem um personagem!")
                return
            
            # Busca o jogador
            jogador = db.query(Jogador).filter_by(usuario_id=usuario.id).first()
            if not jogador:
                await ctx.send("❌ Erro: personagem não encontrado!")
                return
            
            # Pega informações da facção
            info_faccao = FACCAO_INFO.get(jogador.faccao, {})
            
            # Cria o embed do perfil
            embed = discord.Embed(
                title=f"⚔️ **PERFIL DE {membro.name.upper()}** ⚔️",
                color=info_faccao.get('cor', Cores.AZUL_FORTE)
            )
            
            # Thumbnail com avatar do usuário
            embed.set_thumbnail(url=membro.display_avatar.url)
            
            # Informações básicas
            info_basica = (
                f"**Facção:** {info_faccao.get('emoji', '')} {info_faccao.get('nome', 'Desconhecida')}\n"
                f"**Nível:** {jogador.nivel}\n"
                f"**XP:** {jogador.xp}\n"
                f"**Berries:** 💰 {jogador.berries}\n"
                f"**Registro:** {usuario.data_registro.strftime('%d/%m/%Y')}"
            )
            embed.add_field(name="📋 **INFORMAÇÕES**", value=info_basica, inline=False)
            
            # Status de combate
            status_combate = (
                f"❤️ **Vida:** {jogador.vida}/{jogador.vida_max}\n"
                f"🛡️ **Armadura:** {jogador.armadura}\n"
                f"⚡ **Velocidade:** {jogador.velocidade}\n"
                f"⚔️ **Vitórias:** {jogador.vitorias}\n"
                f"💔 **Derrotas:** {jogador.derrotas}"
            )
            embed.add_field(name="⚔️ **COMBATE**", value=status_combate, inline=True)
            
            # Estilos de luta
            estilos = (
                f"👊 **Soco:** {jogador.soco}\n"
                f"⚔️ **Espada:** {jogador.espada}\n"
                f"🔫 **Arma:** {jogador.arma}\n"
                f"🍎 **Fruta:** {jogador.fruta}"
            )
            embed.add_field(name="🥋 **HABILIDADES**", value=estilos, inline=True)
            
            # Hakis
            hakis = (
                f"🛡️ **Armamento:** {jogador.haki_armamento}\n"
                f"👁️ **Observação:** {jogador.haki_observacao}\n"
                f"👑 **Rei:** {jogador.haki_rei}"
            )
            embed.add_field(name="🌀 **HAKIS**", value=hakis, inline=True)
            
            # Barra de XP
            xp_proximo = jogador.nivel * 100
            xp_atual = jogador.xp
            percentual = min(100, int((xp_atual / xp_proximo) * 100))
            
            barra = "🟩" * (percentual // 10) + "⬜" * (10 - (percentual // 10))
            
            embed.add_field(
                name="📊 **PROGRESSÃO**",
                value=f"**Nível {jogador.nivel}**\n{barra} {percentual}%\n`{xp_atual}/{xp_proximo} XP`",
                inline=False
            )
            
            # Footer
            embed.set_footer(text=f"ID: {jogador.id} • Use o menu abaixo para navegar")
            
            # ===== MENU INTERATIVO =====
            view = PerfilMenuView(ctx.author.id, jogador, self.bot)
            
            await ctx.send(embed=embed, view=view)
            
        except Exception as e:
            await ctx.send(f"❌ Erro ao carregar perfil: ```{str(e)}```")
        finally:
            db.close()
    
    @commands.command(name="rank", aliases=["ranking", "top"])
    async def rank(self, ctx):
        """Mostra o ranking dos jogadores"""
        
        db = SessionLocal()
        try:
            # Busca top 10 jogadores por nível
            top_jogadores = db.query(Jogador).order_by(
                Jogador.nivel.desc(),
                Jogador.xp.desc()
            ).limit(10).all()
            
            if not top_jogadores:
                await ctx.send("❌ Nenhum jogador encontrado!")
                return
            
            embed = discord.Embed(
                title="🏆 **RANKING GRAND LINE** 🏆",
                description="Os guerreiros mais poderosos dos mares:",
                color=Cores.DOURADO
            )
            
            medalhas = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            
            ranking_text = ""
            for i, jogador in enumerate(top_jogadores):
                usuario = db.query(Usuario).filter_by(id=jogador.usuario_id).first()
                if usuario:
                    info = FACCAO_INFO.get(jogador.faccao, {})
                    medalha = medalhas[i] if i < len(medalhas) else "•"
                    
                    ranking_text += (
                        f"{medalha} **{usuario.nome_discord}** {info.get('emoji', '')}\n"
                        f"┗ Nv.{jogador.nivel} | ⚔️ {jogador.vitorias} vitórias | 💰 {jogador.berries} berries\n"
                    )
            
            embed.add_field(name="⚔️ **TOP 10 PIRATAS**", value=ranking_text, inline=False)
            embed.set_footer(text="Use !perfil @usuário para ver detalhes")
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Erro ao carregar ranking: ```{str(e)}```")
        finally:
            db.close()

async def setup(bot):
    await bot.add_cog(PerfilCog(bot))