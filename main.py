import discord
from discord.ext import commands
import config
import asyncio
import sys
import io

# Configurar saída para UTF-8 no Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'[OK] Bot conectado como {bot.user.name}')
    print(f'[ID] {bot.user.id}')
    print(f'[Servidores] {len(bot.guilds)}')
    
    # Lista todos os comandos carregados
    print('\n[Comandos disponíveis]:')
    for cmd in bot.commands:
        print(f'   • !{cmd.name}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return  # Ignora comandos não encontrados
    raise error

async def load_cogs():
    cogs = [
        'cogs.registro',
        'cogs.perfil', 
        'cogs.tutorial_combate',
        'cogs.racas'
    ]
    
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            print(f'[OK] {cog} carregado!')
        except Exception as e:
            print(f'[ERRO] ao carregar {cog}: {e}')
            print(f'   Tipo: {type(e).__name__}')
            print(f'   Detalhes: {e}')
            sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(load_cogs())
        bot.run(config.TOKEN)
    except KeyboardInterrupt:
        print("\n[OFF] Bot desligado pelo usuário")
    except Exception as e:
        print(f"[ERRO FATAL] {e}")