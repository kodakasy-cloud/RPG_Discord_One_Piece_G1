import discord
from ui.cores import Cores
from database.connection import SessionLocal
from dados_ilha import ILHAS

# ===== BOTÕES DO MENU PRINCIPAL DA ILHA =====
class ExplorarButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🔍 EXPLORAR", style=discord.ButtonStyle.success, row=1)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        await self.main_view.menu_explorar(interaction)


class HistoriaButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="📜 HISTÓRIA", style=discord.ButtonStyle.danger, row=1)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        ilha = ILHAS.get(self.main_view.ilha_atual, ILHAS["inicial"])
        
        historia = f"**História da {ilha['nome']}**\n\nUma ilha com tradições antigas e segredos a serem descobertos...\n\n🚧 **Em desenvolvimento!**"
        
        embed = discord.Embed(
            title="📜 HISTÓRIA",
            description=historia,
            color=Cores.VERMELHO_FORTE
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=8)


class ProcuradosButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="👀 PROCURADOS", style=discord.ButtonStyle.danger, row=1)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        # Por enquanto não faz nada (conforme solicitado)
        embed = discord.Embed(
            title="👀 PROCURADOS",
            description="🚧 **Em desenvolvimento!**",
            color=Cores.VERMELHO_FORTE
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=3)


class BarButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🍺 BAR", style=discord.ButtonStyle.secondary, row=2)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🍺 BAR",
            description="Você entra no bar local...\n\n🚧 **Em desenvolvimento!**",
            color=Cores.LARANJA_FORTE
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)


class HotelButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🏨 HOTEL", style=discord.ButtonStyle.secondary, row=2)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        # Cura o jogador
        self.jogador.vida = self.jogador.vida_max
        self.jogador.energia = self.jogador.energia_max
        
        db = SessionLocal()
        try:
            db.add(self.jogador)
            db.commit()
        finally:
            db.close()
        
        embed = discord.Embed(
            title="🏨 HOTEL",
            description=f"Você descansou no hotel e recuperou toda sua vida e energia!\n\n❤️ **Vida:** {self.jogador.vida}/{self.jogador.vida_max}\n⚡ **Energia:** {self.jogador.energia}/{self.jogador.energia_max}",
            color=Cores.VERDE_CLARO
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=5)


class VoltarIlhaButton(discord.ui.Button):
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


class VoltarAoPerfilButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🏠 PERFIL", style=discord.ButtonStyle.primary, row=3)
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


# ===== BOTÕES DO MENU DE EXPLORAÇÃO =====
class FlorestaButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🌲 FLORESTA", style=discord.ButtonStyle.primary, row=1)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🌲 FLORESTA",
            description="Uma densa floresta cheia de mistérios. Dizem que criaturas selvagens e tesouros escondidos podem ser encontrados aqui.\n\n**Possíveis encontros:**\n• Animais selvagens\n• Caçadores\n• Tesouros escondidos\n\n🚧 **Em desenvolvimento!**",
            color=Cores.VERDE_CLARO
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=8)


class CavernaButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🪨 CAVERNA", style=discord.ButtonStyle.primary, row=1)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🪨 CAVERNA",
            description="Uma caverna escura e úmida. O eco de seus passos é a única companhia...\n\n**Possíveis encontros:**\n• Morcegos gigantes\n• Mineradores\n• Minérios raros\n\n🚧 **Em desenvolvimento!**",
            color=Cores.CINZA_CLARO
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=8)


class PraiaButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🏖️ PRAIA", style=discord.ButtonStyle.primary, row=1)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🏖️ PRAIA",
            description="Uma bela praia de areia branca e águas cristalinas. Perfeita para relaxar ou... pescar?\n\n**Possíveis encontros:**\n• Peixes exóticos\n• Tesouros enterrados\n• Piratas\n\n🚧 **Em desenvolvimento!**",
            color=Cores.AZUL_FORTE
        )
        await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=8)


class CidadeButton(discord.ui.Button):
    def __init__(self, user_id, jogador, bot, view):
        super().__init__(label="🏙️ CIDADE", style=discord.ButtonStyle.secondary, row=2)
        self.user_id = user_id
        self.jogador = jogador
        self.bot = bot
        self.main_view = view
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Não é seu perfil!", ephemeral=True)
            return
        
        # Volta para o menu da ilha (cidade)
        await self.main_view.menu_ilha(interaction)