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
    
    @commands.command(name="registrar", aliases=["iniciar", "comecar", "aventura", "novo", "joinha", "op"])
    async def registrar(self, ctx):
        """Inicie sua jornada no Grand Line"""
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
            description="**UMA LENDA ESTÁ PRESTES A NASCER...**",
            color=Cores.DOURADO
        )
        
        # ENVIA a primeira mensagem e guarda em msg
        msg = await ctx.send(embed=embed)
        
        # Sequência de mensagens (editando a mesma msg)
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
            title="⚜️ 𝐆𝐑𝐀𝐍𝐃 𝐋𝐈𝐍𝐄 𝐀𝐃𝐕𝐄𝐍𝐓𝐔𝐑𝐄 ⚜️",
            description=(
                f"\n"
                "```\n"
                "⚔️  𝐒𝐔𝐀 𝐋𝐄𝐍𝐃𝐀 𝐂𝐎𝐌𝐄Ç𝐀 𝐀𝐆𝐎𝐑𝐀  ⚔️\n"
                "```\n\n"
                "👑 **O título de Rei dos Piratas está vazio.**\n"
                "🌊 **Os mares infinitos te aguardam.**\n"
                "⚔️ **Aventureiros vieram e se foram.**\n"
                "✨ **Mas lendas... lendas são para sempre.**\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "**🔥 VOCÊ NASCEU PARA SER LENDA! 🔥**"
            ),
            color=Cores.DOURADO
        )
        
        embed.set_footer(text="Clique no botão abaixo para iniciar sua jornada")
        
        view = IniciarView(user_id)
        await msg.edit(embed=embed, view=view)  # ← msg está definida aqui
        
        # Timeout
        await asyncio.sleep(120)
        if user_id in self.registros_ativos:
            del self.registros_ativos[user_id]

async def setup(bot):
    await bot.add_cog(RegistroCog(bot))