import discord
from views.buttons.inventario import *

async def show_menu_inventario(view, interaction: discord.Interaction):
    """Abre o menu de inventário"""
    view.clear_items()
    view.add_item(ItensButton(view.user_id, view.jogador, view.bot))
    view.add_item(HabilidadesButton(view.user_id, view.jogador, view.bot))
    view.add_item(RacaSobrenomeButton(view.user_id, view.jogador, view.bot, view))
    view.add_item(VoltarButton(view.user_id, view.jogador, view.bot, view))
    await interaction.response.edit_message(view=view)