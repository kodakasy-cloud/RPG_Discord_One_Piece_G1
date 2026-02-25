import discord
from discord.ext import commands
import config
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f' Bot conectado como {bot.user.name}')
    print(f' ID: {bot.user.id}')
    print(f' Servidores: {len(bot.guilds)}')

async def load_cogs():
    try:
        await bot.load_extension('cogs.registro')
        await bot.load_extension('cogs.perfil')
        await bot.load_extension('cogs.tutorial_combate')
        await bot.load_extension('cogs.racas')
        
        print(' Cog registrar carregado!')
        print(' Cog perfil carregado!') 
        print(' Cog tutorial carregado!') 
        print(' Cog raças carregado!') 
        
    except Exception as e:
        print(f' Erro ao carregar: {e}')

if __name__ == "__main__":
    asyncio.run(load_cogs())
    bot.run(config.TOKEN)