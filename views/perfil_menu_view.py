# views/perfil_menu_view.py
import discord
from ui.cores import Cores

class PerfilMenuView(discord.ui.View):
    """Menu interativo do perfil com várias opções"""
    
    def __init__(self, user_id, jogador, bot):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
    
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
    
    # ===== LINHA 1 =====
    @discord.ui.button(label="🚶 ANDAR PELA ILHA", style=discord.ButtonStyle.primary, row=0)
    async def andar_ilha(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "🚶 Explorar a Ilha",
            "Você começa a explorar a ilha...\n\n🚧 **Em desenvolvimento!**",
            Cores.AZUL_FORTE
        )
    
    @discord.ui.button(label="⛵ NAVEGAR", style=discord.ButtonStyle.primary, row=0)
    async def navegar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "⛵ Navegar pelos Mares",
            "Você parte para o mar em busca de novas ilhas...\n\n🚧 **Em desenvolvimento!**",
            Cores.AZUL_FORTE
        )
    
    @discord.ui.button(label="🎒 INVENTÁRIO", style=discord.ButtonStyle.primary, row=0)
    async def inventario(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "🎒 Inventário",
            f"**Seus itens:**\n\n💰 Berries: {self.jogador.berries}\n📦 Nenhum item no momento\n\n🚧 **Em desenvolvimento!**",
            Cores.VERDE_CLARO
        )
    
    # ===== LINHA 2 =====
    @discord.ui.button(label="🖤 BLACK MARKET", style=discord.ButtonStyle.secondary, row=1)
    async def black_market(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "🖤 Black Market",
            "Você entra no mercado negro...\n\n🚧 **Em desenvolvimento!**",
            Cores.VERMELHO_FORTE
        )
    
    @discord.ui.button(label="🍺 BAR", style=discord.ButtonStyle.secondary, row=1)
    async def bar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "🍺 Bar da Vila",
            "Você entra no bar e pede uma bebida...\n\n🚧 **Em desenvolvimento!**",
            Cores.LARANJA_FORTE
        )
    
    @discord.ui.button(label="⚔️ HABILIDADES", style=discord.ButtonStyle.secondary, row=1)
    async def habilidades(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Mostra as habilidades atuais do jogador
        habilidades_text = (
            f"**Habilidades disponíveis:**\n\n"
            f"👊 **Soco:** Nível {self.jogador.soco}\n"
            f"⚔️ **Espada:** Nível {self.jogador.espada}\n"
            f"🔫 **Arma:** Nível {self.jogador.arma}\n"
            f"🍎 **Fruta:** Nível {self.jogador.fruta}\n\n"
            f"🌀 **Hakis:**\n"
            f"🛡️ Armamento: {self.jogador.haki_armamento}\n"
            f"👁️ Observação: {self.jogador.haki_observacao}\n"
            f"👑 Rei: {self.jogador.haki_rei}\n\n"
            f"🚧 **Sistema em desenvolvimento!**"
        )
        
        await self.mostrar_mensagem_temporaria(
            interaction,
            "⚔️ Habilidades",
            habilidades_text,
            Cores.DOURADO,
            5
        )
    
    # ===== LINHA 3 =====
    @discord.ui.button(label="🧬 RAÇA E SOBRENOMES", style=discord.ButtonStyle.success, row=2)
    async def raca_sobrenomes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "🧬 Raça e Sobrenomes",
            "Você verifica sua linhagem...\n\n🚧 **Em desenvolvimento!**",
            Cores.VERDE_CLARO
        )
    
    @discord.ui.button(label="⚙️ CONFIGURAÇÃO", style=discord.ButtonStyle.success, row=2)
    async def configuracao(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.mostrar_mensagem_temporaria(
            interaction,
            "⚙️ Configurações",
            "Opções de configuração do personagem:\n\n"
            "• Alterar descrição\n"
            "• Escolher título\n"
            "• Ajustes de notificações\n\n"
            "🚧 **Em desenvolvimento!**",
            Cores.CINZA_CLARO
        )
    
    @discord.ui.button(label="🚪 SAIR", style=discord.ButtonStyle.danger, row=2)
    async def sair(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Desabilita todos os botões
        for item in self.children:
            item.disabled = True
        
        embed = discord.Embed(
            title="👋 Até logo!",
            description="Use `!perfil` novamente quando quiser voltar.",
            color=Cores.VERMELHO_FORTE
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        """Quando o menu expira (120 segundos)"""
        for item in self.children:
            item.disabled = True
        
        if hasattr(self, 'mensagem_original'):
            embed = discord.Embed(
                title="⏰ Menu Expirado",
                description="Use `!perfil` novamente para abrir o menu.",
                color=Cores.AMARELO
            )
            await self.mensagem_original.edit(embed=embed, view=self)