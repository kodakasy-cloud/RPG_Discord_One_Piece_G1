import discord
from ui.cores import Cores
from views.buttons.ilha import *

async def show_menu_explorar(view, interaction: discord.Interaction):
    """Abre o menu de exploração com os locais disponíveis"""
    view.clear_items()
    
    # Pega informações da ilha atual
    from dados_ilha import ILHAS
    ilha = ILHAS.get(view.ilha_atual, ILHAS["inicial"])
    
    # Cria embed explicando a exploração
    embed = discord.Embed(
        title=f"🔍 **EXPLORAR {ilha['nome'].upper()}**",
        description="Escolha um local para explorar. Cada área oferece desafios e recompensas diferentes.",
        color=Cores.VERDE_CLARO
    )
    
    # Descrição dos locais
    locais = (
        "**🌲 FLORESTA** - Enfrente animais selvagens e encontre tesouros\n"
        "**🪨 CAVERNA** - Descubra minérios raros e criaturas das trevas\n"
        "**🏖️ PRAIA** - Pesque, procure tesouros e lute contra piratas\n\n"
        "**🏙️ CIDADE** - Volte para a cidade\n"
        "**🏠 PERFIL** - Volte para seu perfil"
    )
    
    embed.add_field(name="📋 **LOCAIS DISPONÍVEIS**", value=locais, inline=False)
    embed.set_footer(text="Escolha um local para explorar")
    
    # Adiciona botões de exploração
    view.add_item(FlorestaButton(view.user_id, view.jogador, view.bot, view))
    view.add_item(CavernaButton(view.user_id, view.jogador, view.bot, view))
    view.add_item(PraiaButton(view.user_id, view.jogador, view.bot, view))
    view.add_item(CidadeButton(view.user_id, view.jogador, view.bot, view))
    view.add_item(VoltarAoPerfilButton(view.user_id, view.jogador, view.bot, view))
    
    await interaction.response.edit_message(embed=embed, view=view)