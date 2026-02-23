# main.py
import discord
from discord.ext import commands
import config
import asyncio

# Configuração dos intents
intents = discord.Intents.default()
intents.message_content = True

# Cria o bot
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f' Bot conectado como {bot.user.name}')
    print(f' ID: {bot.user.id}')
    print(f' Servidores: {len(bot.guilds)}')

async def load_cogs():
    try:
        await bot.load_extension('cogs.registro')
        print(' Cog registro carregado!')
    except Exception as e:
        print(f' Erro: {e}')

@bot.command(name="teste")
async def teste(ctx):
    await ctx.send("Comando teste funcionando!")

if __name__ == "__main__":
    asyncio.run(load_cogs())
    bot.run(config.TOKEN)