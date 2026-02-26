import discord
from ui.cores import Cores

class PerfilMenuView(discord.ui.View):
    """Menu interativo do perfil com navegação entre telas"""
    
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
    
    async def menu_principal(self, interaction: discord.Interaction):
        """Volta para o menu principal"""
        self.clear_items()
        
        # LINHA 0
        self.add_item(IlhaButton(self.user_id, self.jogador, self.bot))
        self.add_item(NavegarButton(self.user_id, self.jogador, self.bot))
        self.add_item(InventarioButton(self.user_id, self.jogador, self.bot, self))
        
        # LINHA 3 (Config e Sair)
        self.add_item(ConfigButton(self.user_id, self.jogador, self.bot))
        self.add_item(SairButton(self.user_id, self.jogador, self.bot))
        
        await interaction.response.edit_message(view=self)
    
    async def menu_inventario(self, interaction: discord.Interaction):
        """Abre o menu de inventário"""
        self.clear_items()
        
        # LINHA 0
        self.add_item(ItensButton(self.user_id, self.jogador, self.bot))
        self.add_item(HabilidadesButton(self.user_id, self.jogador, self.bot))
        self.add_item(RacaSobrenomeButton(self.user_id, self.jogador, self.bot, self))
        
        # LINHA 3 (Voltar)
        self.add_item(VoltarButton(self.user_id, self.jogador, self.bot, self))
        
        await interaction.response.edit_message(view=self)


# ===== BOTÕES DO MENU PRINCIPAL =====
class IlhaButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot):
        super().__init__(label="🏝️ ILHA", style=discord.ButtonStyle.primary, row=0)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🏝️ ILHA",
            description="🚧 **Em desenvolvimento!**",
            color=Cores.AZUL_FORTE
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=3)


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


# ===== BOTÕES DO MENU DE INVENTÁRIO =====
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
        
        # Abre o sistema de raças (substitui a mensagem atual)
        await self.main_view.abrir_sistema_racas(interaction)


class VoltarButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🚪 VOLTAR", style=discord.ButtonStyle.secondary, row=3)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        await self.main_view.menu_principal(interaction)


# View principal (agora mais simples)
class PerfilMenuView(discord.ui.View):
    def __init__(self, user_id, jogador, bot):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.mensagem_original = None
        
        # Menu inicial
        self.add_item(IlhaButton(user_id, jogador, bot))
        self.add_item(NavegarButton(user_id, jogador, bot))
        self.add_item(InventarioButton(user_id, jogador, bot, self))
        self.add_item(ConfigButton(user_id, jogador, bot))
        self.add_item(SairButton(user_id, jogador, bot))
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id
    
    async def menu_principal(self, interaction: discord.Interaction):
        """Volta para o menu principal"""
        self.clear_items()
        self.add_item(IlhaButton(self.user_id, self.jogador, self.bot))
        self.add_item(NavegarButton(self.user_id, self.jogador, self.bot))
        self.add_item(InventarioButton(self.user_id, self.jogador, self.bot, self))
        self.add_item(ConfigButton(self.user_id, self.jogador, self.bot))
        self.add_item(SairButton(self.user_id, self.jogador, self.bot))
        await interaction.response.edit_message(view=self)
    
    async def menu_inventario(self, interaction: discord.Interaction):
        """Abre o menu de inventário"""
        self.clear_items()
        self.add_item(ItensButton(self.user_id, self.jogador, self.bot))
        self.add_item(HabilidadesButton(self.user_id, self.jogador, self.bot))
        self.add_item(RacaSobrenomeButton(self.user_id, self.jogador, self.bot, self))
        self.add_item(VoltarButton(self.user_id, self.jogador, self.bot, self))
        await interaction.response.edit_message(view=self)
    
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
            await self.menu_principal(interaction)
    
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