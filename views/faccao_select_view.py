import discord
from discord.ui import Select, View, Button
from ui.cores import Cores
from data.faccao_config import FACCAO_INFO
from data.data_fac_info import FACCOES
from views.confirmacao_view import ConfirmacaoView

class FaccaoSelect(Select):
    def __init__(self, user_id, nome_usuario, raca_info, sobrenome_info, bot):
        self.user_id = user_id
        self.nome_usuario = nome_usuario
        self.raca_info = raca_info
        self.sobrenome_info = sobrenome_info
        self.bot = bot
        
        options = []
        for key, faccao in FACCAO_INFO.items():
            stats = FACCOES.get(key, {})
            vida = stats.get('vida', 0)
            armadura = stats.get('armadura', 0)
            velocidade = stats.get('velocidade', 0)
            
            options.append(
                discord.SelectOption(
                    label=faccao["nome"],
                    description=f"❤️ {vida} | 🛡️ {armadura} | 🏃 {velocidade}",
                    emoji=faccao["emoji"],
                    value=key
                )
            )
        
        super().__init__(
            placeholder="⚔️ Escolha sua facção...",
            min_values=1,
            max_values=1,
            options=options
        )
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Este registro não é para você!", ephemeral=True)
            return
        
        faccao_key = self.values[0]
        await self.mostrar_detalhes_faccao(interaction, faccao_key)
    
    async def mostrar_detalhes_faccao(self, interaction, faccao_key):
        faccao = FACCAO_INFO[faccao_key]
        stats_faccao = FACCOES.get(faccao_key, {})
        
        # Calcula status finais
        bonus_raca = self.raca_info['info'].get('bonus', {})
        bonus_sobrenome = self.sobrenome_info['info'].get('bonus', {})
        
        vida_total = 10 + stats_faccao.get('vida', 0) + bonus_raca.get('vida', 0) + bonus_sobrenome.get('vida', 0)
        armadura_total = 5 + stats_faccao.get('armadura', 0) + bonus_raca.get('armadura', 0) + bonus_sobrenome.get('armadura', 0)
        velocidade_total = 10 + stats_faccao.get('velocidade', 0) + bonus_raca.get('velocidade', 0) + bonus_sobrenome.get('velocidade', 0)
        
        embed = discord.Embed(
            title=f"{faccao['emoji']} **{faccao['nome']}**",
            description=faccao['descricao'],
            color=faccao['cor']
        )
        
        preview = (
            f"❤️ **Vida:** {vida_total}\n"
            f"🛡️ **Armadura:** {armadura_total}\n"
            f"🏃 **Velocidade:** {velocidade_total}"
        )
        embed.add_field(name="📊 **STATUS FINAIS**", value=preview, inline=False)
        
        embed.add_field(
            name="👤 **SEU PERSONAGEM**",
            value=(
                f"**Raça:** {self.raca_info['info']['nome']}\n"
                f"**Sobrenome:** {self.sobrenome_info['info']['nome']}"
            ),
            inline=False
        )
        
        embed.set_footer(text="Confirme sua escolha ou volte para escolher outra facção:")
        
        # View com botões de confirmar, voltar e cancelar
        view = FaccaoDetalhesView(
            self.user_id,
            self.nome_usuario,
            faccao_key,
            self.raca_info,
            self.sobrenome_info,
            self.bot
        )
        
        await interaction.response.edit_message(embed=embed, view=view)


class FaccaoDetalhesView(View):
    def __init__(self, user_id, nome_usuario, faccao, raca_info, sobrenome_info, bot):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.nome_usuario = nome_usuario
        self.faccao = faccao
        self.raca_info = raca_info
        self.sobrenome_info = sobrenome_info
        self.bot = bot
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Esta escolha não é para você!", ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="✅ CONFIRMAR", style=discord.ButtonStyle.success, row=0)
    async def confirmar(self, interaction: discord.Interaction, button: Button):
        """Confirma a escolha da facção"""
        view = ConfirmacaoView(
            self.user_id,
            self.nome_usuario,
            self.faccao,
            self.raca_info,
            self.sobrenome_info
        )
        
        # Pega a facção escolhida
        from data.faccao_config import FACCAO_INFO
        faccao = FACCAO_INFO[self.faccao]
        
        embed = discord.Embed(
            title=f"{faccao['emoji']} **{faccao['nome']}**",
            description="Tem certeza que deseja escolher esta facção?",
            color=faccao['cor']
        )
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label="🔙 VOLTAR", style=discord.ButtonStyle.secondary, emoji="🔙", row=0)
    async def voltar(self, interaction: discord.Interaction, button: Button):
        """Volta para a lista de facções"""
        
        # Recria o select original
        embed = discord.Embed(
            title="🎲 **ESCOLHA SUA FACÇÃO**",
            description="Selecione uma facção no menu abaixo:",
            color=Cores.DOURADO
        )
        
        # Mostra novamente os resultados do sorteio
        bonus_raca = " • ".join([f"+{v} {k}" for k, v in self.raca_info['info']['bonus'].items()])
        bonus_sobrenome = " • ".join([f"+{v} {k}" for k, v in self.sobrenome_info['info']['bonus'].items()])
        
        embed.add_field(
            name=f"{self.raca_info['info']['emoji']} **SUA RAÇA**",
            value=f"**{self.raca_info['info']['nome']}**\n`{bonus_raca}`",
            inline=True
        )
        
        embed.add_field(
            name=f"{self.sobrenome_info['info']['emoji']} **SEU SOBRENOME**",
            value=f"**{self.sobrenome_info['info']['nome']}**\n`{bonus_sobrenome}`",
            inline=True
        )
        
        embed.set_footer(text="Escolha sua facção para continuar:")
        
        # Recria a view original com o select
        view = FaccaoSelectView(
            self.user_id,
            self.nome_usuario,
            self.raca_info,
            self.sobrenome_info,
            self.bot
        )
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(label="❌ CANCELAR", style=discord.ButtonStyle.danger, row=0)
    async def cancelar(self, interaction: discord.Interaction, button: Button):
        """Cancela todo o registro"""
        embed = discord.Embed(
            title="❌ **REGISTRO CANCELADO**",
            description="Use `!registrar` quando quiser tentar novamente.",
            color=Cores.VERMELHO_FORTE
        )
        
        for item in self.children:
            item.disabled = True
            
        await interaction.response.edit_message(embed=embed, view=self)


class FaccaoSelectView(View):
    def __init__(self, user_id, nome_usuario, raca_info, sobrenome_info, bot):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.nome_usuario = nome_usuario
        self.raca_info = raca_info
        self.sobrenome_info = sobrenome_info
        self.bot = bot
        self.message = None
        self.add_item(FaccaoSelect(user_id, nome_usuario, raca_info, sobrenome_info, bot))
        
        # Adiciona botão de cancelar direto na tela inicial também
        cancel_button = Button(label="❌ CANCELAR", style=discord.ButtonStyle.danger, row=1)
        cancel_button.callback = self.cancelar_callback
        self.add_item(cancel_button)
    
    async def cancelar_callback(self, interaction: discord.Interaction):
        """Cancela o registro"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Este registro não é para você!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="❌ **REGISTRO CANCELADO**",
            description="Use `!registrar` quando quiser tentar novamente.",
            color=Cores.VERMELHO_FORTE
        )
        
        for item in self.children:
            item.disabled = True
            
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        
        if self.message:
            embed = discord.Embed(
                title="⏰ **TEMPO ESGOTADO**",
                description="Use `!registrar` novamente.",
                color=Cores.VERMELHO_FORTE
            )
            await self.message.edit(embed=embed, view=self)