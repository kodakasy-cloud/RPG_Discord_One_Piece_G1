import discord
from ui.cores import Cores

class ItensButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot):
        super().__init__(label="📦 ITENS", style=discord.ButtonStyle.secondary, row=0)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="📦 ITENS",
            description=f"💰 Berries: {self.jogador.berries}\n📦 Nenhum item no inventário.",
            color=Cores.VERDE_CLARO
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)


class HabilidadesButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot):
        super().__init__(label="⚔️ HABILIDADES", style=discord.ButtonStyle.secondary, row=0)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        texto = (
            f"👊 **Soco:** {self.jogador.soco}\n"
            f"⚔️ **Espada:** {self.jogador.espada}\n"
            f"🔫 **Arma:** {self.jogador.arma}\n"
            f"🍎 **Fruta:** {self.jogador.fruta}"
        )
        
        embed = discord.Embed(
            title="⚔️ HABILIDADES",
            description=texto,
            color=Cores.DOURADO
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)


class RacaSobrenomeButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🧬 RAÇA/SOBRENOME", style=discord.ButtonStyle.success, row=0)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        await self.main_view.abrir_sistema_racas(interaction)


class VoltarButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🚪 VOLTAR", style=discord.ButtonStyle.secondary, row=2)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        # Volta para o perfil normal
        await self.main_view.mostrar_perfil_normal(interaction)