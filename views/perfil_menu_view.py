import discord
from ui.cores import Cores

class PerfilMenuView(discord.ui.View):
    """Menu interativo do perfil com várias opções"""
    
    def __init__(self, user_id, jogador, bot):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.mensagem_original = None
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Verifica se é o dono do perfil"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Você só pode interagir com seu próprio perfil!", ephemeral=True)
            return False
        return True
    
    async def mostrar_mensagem_temporaria(self, interaction: discord.Interaction, titulo: str, descricao: str, cor, tempo: int = 3):
        """Mostra uma mensagem temporária"""
        embed = discord.Embed(
            title=titulo,
            description=descricao,
            color=cor
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=tempo)
    
    async def abrir_sistema_racas(self, interaction: discord.Interaction):
        """Abre o sistema de raças e sobrenomes"""
        
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
            for item in self.children:
                item.disabled = False
            await interaction.edit_original_response(view=self)
    
    # ===== LINHA 1 - AÇÕES =====
    @discord.ui.button(label="🏝️ ILHA", style=discord.ButtonStyle.primary, row=0)
    async def andar_ilha(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "🏝️ ILHA",
            "🚧 **Em desenvolvimento!**",
            Cores.AZUL_FORTE
        )
    
    @discord.ui.button(label="⛵ NAVEGAR", style=discord.ButtonStyle.primary, row=0)
    async def navegar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "⛵ NAVEGAR",
            "🚧 **Em desenvolvimento!**",
            Cores.AZUL_FORTE
        )
    
    @discord.ui.button(label="🎒 INVENTÁRIO", style=discord.ButtonStyle.primary, row=0)
    async def inventario(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "🎒 INVENTÁRIO",
            f"💰 Berries: {self.jogador.berries}\n📦 Nenhum item",
            Cores.VERDE_CLARO
        )
    
    # ===== LINHA 2 - SOCIAL =====
    @discord.ui.button(label="🖤 MERCADO", style=discord.ButtonStyle.secondary, row=1)
    async def black_market(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "🖤 MERCADO NEGRO",
            "🚧 **Em desenvolvimento!**",
            Cores.VERMELHO_FORTE
        )
    
    @discord.ui.button(label="🍺 BAR", style=discord.ButtonStyle.secondary, row=1)
    async def bar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "🍺 BAR",
            "🚧 **Em desenvolvimento!**",
            Cores.LARANJA_FORTE
        )
    
    @discord.ui.button(label="⚔️ HABILIDADES", style=discord.ButtonStyle.secondary, row=1)
    async def habilidades(self, interaction: discord.Interaction, button: discord.ui.Button):
        texto = (
            f"👊 **Soco:** {self.jogador.soco}\n"
            f"⚔️ **Espada:** {self.jogador.espada}\n"
            f"🔫 **Arma:** {self.jogador.arma}\n"
            f"🍎 **Fruta:** {self.jogador.fruta}"
        )
        
        await self.mostrar_mensagem_temporaria(
            interaction,
            "⚔️ HABILIDADES",
            texto,
            Cores.DOURADO,
            5
        )
    
    # ===== LINHA 3 - PERSONALIZAÇÃO =====
    @discord.ui.button(label="🧬 RAÇA", style=discord.ButtonStyle.success, row=2)
    async def raca_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Abre o sistema de raças"""
        await self.abrir_sistema_racas(interaction)
    
    @discord.ui.button(label="📜 SOBRENOME", style=discord.ButtonStyle.success, row=2)
    async def sobrenome_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Abre o sistema de sobrenomes"""
        await self.abrir_sistema_racas(interaction)
    
    @discord.ui.button(label="⚙️ CONFIG", style=discord.ButtonStyle.success, row=2)
    async def configuracao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "⚙️ CONFIGURAÇÕES",
            "🚧 **Em desenvolvimento!**",
            Cores.CINZA_CLARO
        )
    
    @discord.ui.button(label="🚪 SAIR", style=discord.ButtonStyle.danger, row=3)
    async def sair(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True
        
        embed = discord.Embed(
            title="👋 Até logo!",
            description="Use `!perfil` quando quiser voltar.",
            color=Cores.VERMELHO_FORTE
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
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