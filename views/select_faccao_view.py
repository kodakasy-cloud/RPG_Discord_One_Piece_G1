# views/select_faccao_view.py
import discord
from ui.cores import Cores
from data.faccao_config import FACCAO_INFO
from utils.faccao_utils import get_stats_faccao
# NÃO importa ConfirmacaoView aqui ainda

class FaccaoSelect(discord.ui.Select):
    def __init__(self, user_id: int):
        self.user_id = user_id
        options = []
        
        for key, info in FACCAO_INFO.items():
            stats = get_stats_faccao(key)
            options.append(
                discord.SelectOption(
                    label=info['nome'],
                    description=f"❤️ {stats.get('vida', 0)} | 🛡️ {stats.get('armadura', 0)} | ⚡ {stats.get('velocidade', 0)}",
                    emoji=info['emoji'],
                    value=key
                )
            )
        
        super().__init__(
            placeholder="⚔️ Escolha sua facção...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Apenas quem iniciou pode escolher!", ephemeral=True)
            return
        
        await mostrar_detalhes_faccao(interaction, self.values[0])


class FaccaoSelectView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.add_item(FaccaoSelect(user_id))



async def mostrar_detalhes_faccao(interaction: discord.Interaction, faccao: str):

    from views.confirmacao_view import ConfirmacaoView
    
    info = FACCAO_INFO[faccao]
    stats = get_stats_faccao(faccao)
    
    embed = discord.Embed(
        title=f"{info['emoji']} {info['nome']}",
        description=f"*{info['descricao']}*",
        color=info['cor']
    )
    
    embed.add_field(name="📖 História", value=info['historia'][:100] + "...", inline=False)
    
    status = (
        f"❤️ Vida: {stats.get('vida', 0)}/{stats.get('vida_max', stats.get('vida', 0))}\n"
        f"🛡️ Armadura: {stats.get('armadura', 0)}\n"
        f"⚡ Velocidade: {stats.get('velocidade', 0)}"
    )
    embed.add_field(name="📊 Status", value=status, inline=True)
    embed.add_field(name="⚔️ Estilo", value=info['estilo'], inline=True)
    embed.add_field(name="✨ Destaque", value=info['destaque'], inline=True)
    
    embed.set_footer(text="Esta será sua jornada. Deseja prosseguir?")
    
    from cogs.registro import RegistroCog
    bot = interaction.client  
    view = ConfirmacaoView(interaction.user.id, faccao, bot)  
    
    await interaction.response.edit_message(embed=embed, view=view)


async def mostrar_selecao_faccao(interaction: discord.Interaction):
    embed = discord.Embed(
        title="⚔️ ESCOLHA SEU DESTINO",
        description="**Quatro caminhos te aguardam. Qual será sua jornada?**\n",
        color=Cores.AZUL_FORTE
    )
    
    faccoes_text = ""
    for key, info in FACCAO_INFO.items():
        stats = get_stats_faccao(key)
        faccoes_text += (
            f"{info['emoji']} **{info['nome']}**\n"
            f"┗ ❤️ {stats.get('vida', 0)} | 🛡️ {stats.get('armadura', 0)} | ⚡ {stats.get('velocidade', 0)}\n"
            f"┗ *{info['estilo']}*\n\n"
        )
    
    embed.add_field(name="Facções", value=faccoes_text, inline=False)
    embed.set_footer(text="Selecione uma facção no menu abaixo para ver detalhes")
    
    view = FaccaoSelectView(interaction.user.id)
    await interaction.edit_original_response(embed=embed, view=view)