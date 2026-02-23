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
        
        embed = discord.Embed(
            title="⚜️ GRAND LINE ADVENTURE",
            description="Clique no botão para começar!",
            color=Cores.DOURADO
        )
        
        view = IniciarView(user_id)
        await ctx.send(embed=embed, view=view)
        
        await asyncio.sleep(120)
        if user_id in self.registros_ativos:
            del self.registros_ativos[user_id]

async def setup(bot):
    await bot.add_cog(RegistroCog(bot))