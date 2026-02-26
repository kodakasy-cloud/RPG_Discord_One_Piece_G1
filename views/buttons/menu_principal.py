import discord
from ui.cores import Cores

class IlhaButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🏝️ ILHA", style=discord.ButtonStyle.primary, row=0)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        await self.main_view.menu_ilha(interaction)


class NavegarButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot):
        super().__init__(label="⛵ NAVEGAR", style=discord.ButtonStyle.primary, row=0)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="⛵ NAVEGAR",
            description="🚧 **Em desenvolvimento!**",
            color=Cores.AZUL_FORTE
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=3)


class InventarioButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🎒 INVENTÁRIO", style=discord.ButtonStyle.primary, row=0)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        await self.main_view.menu_inventario(interaction)


class ConfigButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot):
        super().__init__(label="⚙️ CONFIG", style=discord.ButtonStyle.success, row=3)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="⚙️ CONFIGURAÇÕES",
            description="🚧 **Em desenvolvimento!**",
            color=Cores.CINZA_CLARO
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=3)


class SairButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot):
        super().__init__(label="🚪 SAIR", style=discord.ButtonStyle.danger, row=3)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        for item in self.view.children:
            item.disabled = True
        
        embed = discord.Embed(
            title="👋 Até logo!",
            description="Use `!perfil` quando quiser voltar.",
            color=Cores.VERMELHO_FORTE
        )
        
        await interaction.response.edit_message(embed=embed, view=self.view)