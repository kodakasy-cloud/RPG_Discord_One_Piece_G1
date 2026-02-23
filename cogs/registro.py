# cogs/registro.py
import discord
from discord.ext import commands
import asyncio
from ui.cores import Cores
from views import IniciarView 

class RegistroCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.registros_ativos = {}
    
    @commands.command(name="registrar")
    async def registrar(self, ctx):
        user_id = ctx.author.id
        
        if user_id in self.registros_ativos:
            await ctx.send("⚠️ Você já tem um registro ativo!")
            return
        
        self.registros_ativos[user_id] = True
        
        intro_messages = [
            ("👑", "O REI DOS PIRATAS, GOLD ROGER...", Cores.DOURADO),
            ("⚔️", "CONQUISTOU TUDO NESTE MUNDO...", Cores.VERMELHO_FORTE),
            ("🏴‍☠️", "SUA ÚLTIMA PALAVRA INSPIROU MILHARES:", Cores.AZUL_FORTE),
            ("💰", "**'MEU TESOURO? SE QUISEREM, PODEM PEGAR!'**", Cores.DOURADO),
            ("🌊", "**'PROCUREM POR ELE! EU DEIXEI TUDO NAQUELE LUGAR!'**", Cores.VERDE_CLARO),
            ("⚜️", "E ASSIM, A GRANDE ERA DOS PIRATAS COMEÇOU...", Cores.LARANJA_FORTE)
        ]
        
        # Primeira mensagem
        embed = discord.Embed(
            description="**UMA LENDA ESTÁ PRESTE A NASCER...**",
            color=Cores.DOURADO
        )
        msg = await ctx.send(embed=embed)
        
        # Sequência de mensagens
        for emoji, texto, cor in intro_messages:
            await asyncio.sleep(2.5)
            embed = discord.Embed(
                description=f"{emoji} **{texto}**",
                color=cor
            )
            await msg.edit(embed=embed)
        
        # Mensagem final com título épico
        await asyncio.sleep(2)
        embed = discord.Embed(
            title="⚜️   Grand Line Adventure    ⚜️",
            description=(
                "```\n"
                "⚔️  O ONE PIECE É REAL!  ⚔️\n"
                "```\n\n"
                "Gold Roger disse:\n"
                "*\"Meu tesouro? Se quiserem, podem pegar!\"*\n\n"
                "🌊 **Séculos se passaram...**\n"
                "⚓ **Milhares navegaram...**\n"
                "👑 **Nenhum encontrou.**\n\n"
                "**🔥 SERÁ QUE VOCÊ SERÁ O ESCOLHIDO? 🔥**"
            ),
            color=Cores.DOURADO
        )
        embed.set_footer(text="Clique no botão abaixo para iniciar sua jornada")
        
        view = IniciarView(user_id)
        await msg.edit(embed=embed, view=view)
        
        # Timeout
        await asyncio.sleep(120)
        if user_id in self.registros_ativos:
            del self.registros_ativos[user_id]

async def setup(bot):
    await bot.add_cog(RegistroCog(bot))