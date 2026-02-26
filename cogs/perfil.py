import discord
from discord.ext import commands
from database.connection import SessionLocal
from models.usuario import Usuario
from models.jogador import Jogador
from data.faccao_config import FACCAO_INFO
from ui.cores import Cores
from views.perfil_menu_view import PerfilMenuView
from datetime import datetime

class PerfilCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def criar_barra_vida(self, valor, maximo, tamanho=5):
        percentual = min(100, int((valor / maximo) * 100))
        cheios = int((percentual / 100) * tamanho)
        return "🟥" * cheios + "⬜" * (tamanho - cheios)
    
    def criar_barra_energia(self, valor, maximo, tamanho=5):
        percentual = min(100, int((valor / maximo) * 100))
        cheios = int((percentual / 100) * tamanho)
        return "🟧" * cheios + "⬜" * (tamanho - cheios)
    
    def criar_barra_xp(self, valor, maximo, tamanho=5):
        percentual = min(100, int((valor / maximo) * 100))
        cheios = int((percentual / 100) * tamanho)
        return "🟩" * cheios + "⬜" * (tamanho - cheios)
    
    @commands.command(name="perfil", aliases=["profile", "status", "stats"])
    async def perfil(self, ctx, membro: discord.Member = None):
        if membro is None:
            membro = ctx.author
        
        db = SessionLocal()
        try:
            usuario = db.query(Usuario).filter_by(
                discord_id=str(membro.id)
            ).first()
            
            if not usuario:
                if membro == ctx.author:
                    await ctx.send("❌ Você ainda não tem um personagem! Use `!registrar`")
                else:
                    await ctx.send(f"❌ {membro.name} não tem personagem!")
                return
            
            jogador = db.query(Jogador).filter_by(usuario_id=usuario.id).first()
            if not jogador:
                await ctx.send("❌ Erro: personagem não encontrado!")
                return
            
            info_faccao = FACCAO_INFO.get(jogador.faccao, {})
            
            embed = discord.Embed(
                title=f"",
                color=info_faccao.get('cor', Cores.AZUL_FORTE)
            )
            
            embed.set_thumbnail(url=membro.display_avatar.url)
            
            raca_text = getattr(jogador, 'raca', None) or "Nenhuma"
            sobrenome_text = getattr(jogador, 'sobrenome', None) or "Nenhum"
            
            # CABEÇALHO
            embed.add_field(name="", value=f"⚔️ {membro.name} • 📜 {sobrenome_text}", inline=False)
            embed.add_field(name="", value=f"{info_faccao.get('emoji', '')} {info_faccao.get('nome', '???')} • 🧬 {raca_text}", inline=False)
            embed.add_field(name="", value="━" * 40, inline=False)
            
            # VIDA E ENERGIA (juntos)
            barra_vida = self.criar_barra_vida(jogador.vida, jogador.vida_max)
            barra_energia = self.criar_barra_energia(jogador.energia, jogador.energia_max)
            embed.add_field(name="", value=f"❤️ {barra_vida} {jogador.vida}/{jogador.vida_max}  ⚡ {barra_energia} {jogador.energia}/{jogador.energia_max}", inline=False)
            embed.add_field(name="", value="━" * 40, inline=False)
            
            # STATUS E HABILIDADES (tudo junto)
            embed.add_field(name="", value="⚔️ STATUS", inline=False)
            embed.add_field(name="", value=f"🛡️ Armadura: {jogador.armadura}  👊 Soco: {jogador.soco} • ⚔️ Espada: {jogador.espada}", inline=False)
            embed.add_field(name="", value=f"🏃 Velocidade: {jogador.velocidade} • 🍎 Fruta: {jogador.fruta} • 🔫 Arma: {jogador.arma}", inline=False)
            embed.add_field(name="", value="━" * 40, inline=False)
            
            # VITÓRIAS E DERROTAS
            embed.add_field(name="", value=f"⚔️ Vitórias: {jogador.vitorias}  💔 Derrotas: {jogador.derrotas}", inline=False)
            embed.add_field(name="", value="━" * 40, inline=False)
            
            # PROGRESSÃO
            xp_proximo = jogador.nivel * 100
            embed.add_field(name="", value=f"💰 B$ {jogador.berries} • NÍVEL {jogador.nivel}", inline=False)
            embed.add_field(name="", value=f"{self.criar_barra_xp(jogador.xp, xp_proximo)} {jogador.xp}/{xp_proximo} XP", inline=False)
            embed.add_field(name="", value="━" * 40, inline=False)
            
            # ID e Data
            embed.add_field(name="", value=f"ID: {jogador.id} • Update v0.5 • {usuario.data_registro.strftime('%d/%m/%Y')}", inline=False)
            
            view = PerfilMenuView(ctx.author.id, jogador, self.bot)
            view.mensagem_original = await ctx.send(embed=embed, view=view)
            
        except Exception as e:
            await ctx.send(f"❌ Erro: ```{str(e)}```")
        finally:
            db.close()
    
    @commands.command(name="rank", aliases=["ranking", "top"])
    async def rank(self, ctx):
        db = SessionLocal()
        try:
            top_jogadores = db.query(Jogador).order_by(
                Jogador.nivel.desc(),
                Jogador.xp.desc()
            ).limit(10).all()
            
            if not top_jogadores:
                await ctx.send("❌ Nenhum jogador encontrado!")
                return
            
            embed = discord.Embed(
                title="🏆 **RANKING**",
                color=Cores.DOURADO
            )
            
            medalhas = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            
            texto = ""
            for i, j in enumerate(top_jogadores):
                user = db.query(Usuario).filter_by(id=j.usuario_id).first()
                if user:
                    medalha = medalhas[i]
                    faccao = FACCAO_INFO.get(j.faccao, {}).get('emoji', '')
                    texto += f"{medalha} **{user.nome_discord}** {faccao}\n"
                    texto += f"┗ Nv.{j.nivel} | ⚔️ {j.vitorias}\n\n"
            
            embed.add_field(name="⚔️ **TOP 10**", value=texto, inline=False)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            await ctx.send(f"❌ Erro: ```{str(e)}```")
        finally:
            db.close()

async def setup(bot):
    await bot.add_cog(PerfilCog(bot))