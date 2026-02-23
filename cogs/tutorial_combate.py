# cogs/tutorial_combate.py
import discord
from discord.ext import commands
import random
import asyncio
from ui.cores import Cores
from data.inimigos_tutorial import INIMIGO_TUTORIAL
from views.batalha_tutorial_view import BatalhaTutorialView
from database.connection import SessionLocal
from models.usuario import Usuario
from models.jogador import Jogador
from pathlib import Path

class TutorialCombateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tutoriais_ativos = {}
    
    @commands.command(name="tutorial", aliases=["treinar", "aprender"])
    async def tutorial(self, ctx):
        """Inicia o tutorial de combate"""
        
        user_id = ctx.author.id
        
        # Verifica se já tem tutorial ativo
        if user_id in self.tutoriais_ativos:
            await ctx.send("⚠️ Você já está em um tutorial! Termine ele primeiro.")
            return
        
        # Busca jogador no banco
        db = SessionLocal()
        try:
            usuario = db.query(Usuario).filter_by(discord_id=str(user_id)).first()
            if not usuario:
                await ctx.send("❌ Você precisa se registrar primeiro! Use `!registrar`")
                return
            
            jogador = db.query(Jogador).filter_by(usuario_id=usuario.id).first()
            if not jogador:
                await ctx.send("❌ Erro ao carregar seu personagem!")
                return
            
        finally:
            db.close()
        
        self.tutoriais_ativos[user_id] = True
        
        # Cria cópia do inimigo para não modificar o original
        inimigo = INIMIGO_TUTORIAL.copy()
        inimigo["vida"] = inimigo["vida_max"]
        
        # ===== TELA DE TUTORIAL - INSTRUÇÕES =====
        embed = discord.Embed(
            title="⚔️ **TUTORIAL DE COMBATE** ⚔️",
            description=f"Bem-vindo, **{ctx.author.name}**!",
            color=Cores.DOURADO
        )
        
        # Instruções resumidas
        instrucoes = (
            "**⚡ SISTEMA DE ENERGIA**\n"
            "┗ Acumule **3⚡** para ataques especiais\n\n"
            
            "**👊 HABILIDADES**\n"
            "┗ **SOCO FORTE** ─── Dano +**1⚡**\n"
            "┗ **PUNHO DE RAIVA** ─── **3x-5x** dano (gasta **3⚡**)\n"
            "┗ **DESVIO** ─── 50% chance esquivar +**3⚡**\n\n"
            
            "**💡 ESTRATÉGIA**\n"
            "┗ Acumule **3⚡** → Use **PUNHO DE RAIVA**"
        )
        
        embed.add_field(
            name="📚 **COMO JOGAR**",
            value=instrucoes,
            inline=False
        )
        
        embed.set_footer(text="Clique no botão abaixo para enfrentar o desafio!")
        
        # Botão para começar
        view = IniciarTutorialView(user_id, jogador, inimigo, self.bot, self)
        
        # Envia a mensagem e guarda a referência
        mensagem = await ctx.send(embed=embed, view=view)
        view.mensagem = mensagem
    
    def finalizar_tutorial(self, user_id):
        """Remove o tutorial da lista de ativos"""
        if user_id in self.tutoriais_ativos:
            del self.tutoriais_ativos[user_id]


class IniciarTutorialView(discord.ui.View):
    def __init__(self, user_id, jogador, inimigo, bot, cog):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.jogador = jogador
        self.inimigo = inimigo
        self.bot = bot
        self.cog = cog
        self.mensagem = None
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id
    
    @discord.ui.button(label="⚔️ COMEÇAR TUTORIAL", style=discord.ButtonStyle.success, emoji="⚡")
    async def comecar(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Desabilita o botão
        button.disabled = True
        await interaction.response.edit_message(view=self)
        
        # ===== A MESMA MENSAGEM É ATUALIZADA PARA A TELA DE SUSPENSE =====
        
        # 1. Aviso que um inimigo apareceu
        embed = discord.Embed(
            description="⚠️ **UM INIMIGO APARECEU!** ⚠️",
            color=Cores.VERMELHO_FORTE
        )
        await self.mensagem.edit(embed=embed, view=None)
        await asyncio.sleep(1.5)
        
        # 2. Fala do inimigo
        embed = discord.Embed(
            description=f"*{self.inimigo['falas']['inicio']}*",
            color=Cores.VERMELHO_FORTE
        )
        await self.mensagem.edit(embed=embed)
        await asyncio.sleep(2)
        
        # 3. Contagem regressiva
        for i in range(3, 0, -1):
            embed = discord.Embed(
                description=f"*{self.inimigo['falas']['inicio']}*\n\n⚔️ **{i}**",
                color=Cores.VERMELHO_FORTE
            )
            await self.mensagem.edit(embed=embed)
            await asyncio.sleep(1)
        
        # 4. Último momento
        embed = discord.Embed(
            description=f"*{self.inimigo['falas']['inicio']}*\n\n🔥 **COMEÇOU!** 🔥",
            color=Cores.VERMELHO_FORTE
        )
        await self.mensagem.edit(embed=embed)
        await asyncio.sleep(0.5)
        
        # ===== INICIA O COMBATE =====
        view = BatalhaTutorialView(
            user_id=self.user_id,
            jogador=self.jogador,
            inimigo=self.inimigo,
            bot=self.bot
        )
        
        # Embed inicial do combate
        embed_combate = discord.Embed(
            title=f"⚔️ **{self.inimigo['nome'].upper()}** ⚔️",
            description=f"*{self.inimigo['descricao']}*",
            color=Cores.AZUL_FORTE
        )
        
        # Status do jogador
        jogador_info = (
            f"💪 **SAUDÁVEL**\n"
            f"\n**VIDA**\n{view.criar_barra_vida(self.jogador.vida, self.jogador.vida_max)}\n"
            f"\n**ENERGIA**\n⚡ {'⚪' * 3} `0/3`\n"
            f"\n👊 **DANO** `{self.jogador.soco}`"
        )
        
        # Status do inimigo
        inimigo_info = (
            f"**\n"
            f"\n**VIDA**\n{view.criar_barra_vida(self.inimigo['vida'], self.inimigo['vida_max'])}\n"
            f"\n**ENERGIA**\n⚡ {'⚪' * 3} `0/3`\n"
            f"\n👊 **DANO** `{self.inimigo['soco']}`"
        )
        
        embed_combate.add_field(name="👤 **JOGADOR**", value=jogador_info, inline=True)
        embed_combate.add_field(name="⚔️ ", value="\u200b\n\u200b\n⚔️\n\u200b\n\u200b", inline=True)
        embed_combate.add_field(name="👾 **INIMIGO**", value=inimigo_info, inline=True)
        
        embed_combate.add_field(name="\u200b", value="━━━━━━━━━━━━━━━━━━━━━━", inline=False)
        embed_combate.add_field(
            name="👾 **FALA DO INIMIGO**", 
            value=f"*{self.inimigo['falas']['inicio']}*", 
            inline=False
        )
        embed_combate.add_field(name="\u200b", value="━━━━━━━━━━━━━━━━━━━━━━", inline=False)
        embed_combate.add_field(name="🎮 **SEU TURNO!**", value="Escolha uma ação abaixo.", inline=False)
        embed_combate.set_footer(text="⏰ 120 segundos para agir")
        
        # Adiciona imagem
        arquivo_imagem = view.get_arquivo_imagem()
        if arquivo_imagem:
            embed_combate.set_thumbnail(url="attachment://bandido.png")
            await self.mensagem.edit(embed=embed_combate, view=view, attachments=[arquivo_imagem])
        else:
            await self.mensagem.edit(embed=embed_combate, view=view)
        
        view.mensagem_combate = self.mensagem
    
    async def on_timeout(self):
        self.cog.finalizar_tutorial(self.user_id)


async def setup(bot):
    await bot.add_cog(TutorialCombateCog(bot))