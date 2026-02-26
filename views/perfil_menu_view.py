import discord
from ui.cores import Cores
from views.buttons.menu_principal import *
from views.buttons.inventario import *
from views.buttons.ilha import *
from views.menus.perfil_normal import show_perfil_normal
from views.menus.menu_inventario import show_menu_inventario
from views.menus.menu_ilha import show_menu_ilha
from views.menus.menu_explorar import show_menu_explorar

class PerfilMenuView(discord.ui.View):
    """Menu interativo do perfil com navegação entre telas"""
    
    def __init__(self, user_id, jogador, bot):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.mensagem_original = None
        self.ilha_atual = "inicial"  # Ilha padrão
        
        # Menu inicial
        self.add_item(IlhaButton(user_id, jogador, bot, self))
        self.add_item(NavegarButton(user_id, jogador, bot))
        self.add_item(InventarioButton(user_id, jogador, bot, self))
        self.add_item(ConfigButton(user_id, jogador, bot))
        self.add_item(SairButton(user_id, jogador, bot))
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id
    
    async def mostrar_perfil_normal(self, interaction: discord.Interaction):
        """Mostra o perfil normal com todas as informações"""
        await show_perfil_normal(self, interaction)
    
    async def menu_inventario(self, interaction: discord.Interaction):
        """Abre o menu de inventário"""
        await show_menu_inventario(self, interaction)
    
    async def menu_ilha(self, interaction: discord.Interaction):
        """Abre o menu da ilha com imagem e descrição"""
        await show_menu_ilha(self, interaction)
    
    async def menu_explorar(self, interaction: discord.Interaction):
        """Abre o menu de exploração"""
        await show_menu_explorar(self, interaction)
    
    async def abrir_sistema_racas(self, interaction: discord.Interaction):
        """Abre o sistema de raças"""
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        
        racas_command = self.bot.get_command('racas')
        
        if racas_command:
            ctx = await self.bot.get_context(interaction.message)
            ctx.author = interaction.user
            ctx.command = racas_command
            
            racas_cog = self.bot.get_cog('Racas')
            
            if racas_cog and hasattr(racas_cog, 'mostrar_menu_racas'):
                await racas_cog.mostrar_menu_racas(interaction, ctx)
            else:
                await self.bot.invoke(ctx)
        else:
            await interaction.followup.send("❌ Sistema de raças não encontrado!", ephemeral=True)
            await self.mostrar_perfil_normal(interaction)
    
    # Métodos auxiliares para criar barras
    def criar_barra_vida(self, valor, maximo, tamanho=5):
        percentual = min(100, int((valor / maximo) * 100))
        cheios = int((percentual / 100) * tamanho)
        return "🟥" * cheios + "⬜" * (tamanho - cheios)
    
    def criar_barra_energia(self, valor, maximo, tamanho=5):
        percentual = min(100, int((valor / maximo) * 100))
        cheios = int((percentual / 100) * tamanho)
        return "🟧" * cheios + "⬜" * (tamanho - cheios)
    
    def criar_barra_xp(self, valor, maximo, tamanho=5):
        percentual = min(100, int((valor / maximo) * 100))
        cheios = int((percentual / 100) * tamanho)
        return "🟩" * cheios + "⬜" * (tamanho - cheios)
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        
        if self.mensagem_original:
            embed = discord.Embed(
                title="⏰ Menu Expirado",
                description="Use `!perfil` novamente.",
                color=Cores.AMARELO
            )
            try:
                await self.mensagem_original.edit(embed=embed, view=self)
            except:
                pass