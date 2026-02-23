import asyncio
import discord
from datetime import datetime

def formatar_timestamp(dt: datetime = None) -> str:
    """
    Formata timestamp para exibição
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%d/%m/%Y %H:%M")


def criar_barra_progresso(valor: int, maximo: int, tamanho: int = 10) -> str:
    """
    Cria uma barra de progresso visual
    Exemplo: "██████░░░░"
    """
    cheios = int((valor / maximo) * tamanho)
    return "█" * cheios + "░" * (tamanho - cheios)


async def enviar_embed_temporario(channel, embed, tempo: int = 5):
    """
    Envia um embed e apaga após alguns segundos
    """
    msg = await channel.send(embed=embed)
    await asyncio.sleep(tempo)
    await msg.delete()