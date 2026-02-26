import discord
from ui.cores import Cores
from dados_ilha import ILHAS
from views.buttons.ilha import *

async def show_menu_ilha(view, interaction: discord.Interaction):
    """Abre o menu da ilha com imagem e descrição"""
    view.clear_items()
    
    # Pega informações da ilha atual
    ilha = ILHAS.get(view.ilha_atual, ILHAS["inicial"])
    
    # Cria embed com imagem
    embed = discord.Embed(
        title=f"🏝️ **{ilha['nome']}**",
        description=ilha['descricao'],
        color=Cores.VERDE_CLARO
    )
    
    # Adiciona imagem
    if ilha.get('imagem'):
        embed.set_image(url=ilha['imagem'])
    
    embed.set_footer(text="Explore a ilha usando os botões abaixo")
    
    # Adiciona botões específicos da ilha
    view.add_item(ExplorarButton(view.user_id, view.jogador, view.bot, view))
    view.add_item(HistoriaButton(view.user_id, view.jogador, view.bot, view))
    view.add_item(ProcuradosButton(view.user_id, view.jogador, view.bot, view))
    view.add_item(BarButton(view.user_id, view.jogador, view.bot, view))
    view.add_item(HotelButton(view.user_id, view.jogador, view.bot, view))
    view.add_item(VoltarIlhaButton(view.user_id, view.jogador, view.bot, view))
    view.add_item(VoltarAoPerfilButton(view.user_id, view.jogador, view.bot, view))
    
    await interaction.response.edit_message(embed=embed, view=view)