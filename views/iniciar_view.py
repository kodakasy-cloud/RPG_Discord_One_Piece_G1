# views/iniciar_view.py
import discord
from ui.cores import Cores
from views.select_faccao_view import mostrar_selecao_faccao  # Import direto

class IniciarView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=120)
        self.user_id = user_id
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            embed = discord.Embed(
                description="❌ **Esta jornada não é sua!**",
                color=Cores.VERMELHO_FORTE
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="🌟 INICIAR JORNADA", style=discord.ButtonStyle.blurple, emoji="⚔️")
    async def iniciar(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        embed = discord.Embed(
            description="⚔️ **Preparando sua aventura...**",
            color=Cores.VERDE_CLARO
        )
        await interaction.response.edit_message(embed=embed, view=self)
        await mostrar_selecao_faccao(interaction)