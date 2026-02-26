import discord
from discord.ext import commands
from ui.cores import Cores
from data.racas import sortear_raca
from data.sobrenomes import sortear_sobrenome
from views.faccao_select_view import FaccaoSelectView
import asyncio

class RegistroCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.registros_ativos = {}
    
    @commands.command(name="registrar", aliases=["criar", "novo"])
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def registrar(self, ctx):
        """Inicia o processo de registro de um novo personagem"""
        
        if ctx.author.id in self.registros_ativos:
            await ctx.send("❌ Você já tem um registro em andamento!", delete_after=5)
            return
        
        self.registros_ativos[ctx.author.id] = True
        
        try:
            # ===== ETAPA 1: SORTEANDO RAÇA =====
            embed_raca = discord.Embed(
                title="🎲 **SORTEANDO RAÇA**",
                description="✨ **Girando a roleta...** ✨",
                color=Cores.AZUL_FORTE
            )
            embed_raca.set_footer(text="Aguarde...")
            
            # Já envia diretamente a primeira tela, sem mensagem inicial
            msg = await ctx.send(embed=embed_raca)
            await asyncio.sleep(3)
            
            # Sorteia a raça
            raca_key, raca_info = sortear_raca()
            
            # Mostra a raça sorteada
            bonus_raca = " • ".join([f"+{v} {k}" for k, v in raca_info['bonus'].items()])
            
            embed_raca_result = discord.Embed(
                title=f"{raca_info['emoji']} **RAÇA SORTEADA**",
                description=f"### {raca_info['nome']}",
                color=Cores.AZUL_FORTE
            )
            
            embed_raca_result.add_field(
                name="📊 **Bônus**",
                value=f"`{bonus_raca}`",
                inline=False
            )
            
            embed_raca_result.set_footer(text="Agora sorteando o sobrenome...")
            await msg.edit(embed=embed_raca_result)
            await asyncio.sleep(3)
            
            # ===== ETAPA 2: SORTEANDO SOBRENOME =====
            embed_sobrenome = discord.Embed(
                title="📜 **SORTEANDO SOBRENOME**",
                description="✨ **Girando a roleta...** ✨",
                color=Cores.ROXO_CLARO
            )
            embed_sobrenome.set_footer(text="Aguarde...")
            await msg.edit(embed=embed_sobrenome)
            await asyncio.sleep(3)
            
            # Sorteia o sobrenome
            sobrenome_key, sobrenome_info = sortear_sobrenome()
            
            # ===== ETAPA 3: RESULTADO FINAL =====
            embed_final = discord.Embed(
                title="🎲 **SORTEIO COMPLETO**",
                description=f"### Parabéns {ctx.author.mention}!",
                color=Cores.DOURADO
            )
            
            # Raça
            bonus_raca = " • ".join([f"+{v} {k}" for k, v in raca_info['bonus'].items()])
            embed_final.add_field(
                name=f"{raca_info['emoji']} **{raca_info['nome']}**",
                value=f"**Bônus:** `{bonus_raca}`",
                inline=True
            )
            
            # Sobrenome
            if sobrenome_key != 'none':
                bonus_sobrenome = " • ".join([f"+{v} {k}" for k, v in sobrenome_info['bonus'].items()])
                embed_final.add_field(
                    name=f"{sobrenome_info['emoji']} **{sobrenome_info['nome']}**",
                    value=f"**Bônus:** `{bonus_sobrenome}`",
                    inline=True
                )
            
            embed_final.set_footer(text="Agora escolha sua facção abaixo:")
            
            # View de escolha de facção
            view = FaccaoSelectView(
                ctx.author.id,
                ctx.author.name,
                {"key": raca_key, "info": raca_info},
                {"key": sobrenome_key, "info": sobrenome_info},
                self.bot
            )
            
            await msg.edit(embed=embed_final, view=view)
            
        finally:
            self.registros_ativos.pop(ctx.author.id, None)
    
    @registrar.error
    async def registrar_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutos = int(error.retry_after // 60)
            segundos = int(error.retry_after % 60)
            
            embed = discord.Embed(
                title="⏳ **AGUARDE**",
                description=f"Tente novamente em **{minutos}min {segundos}s**.",
                color=Cores.VERMELHO_FORTE
            )
            await ctx.send(embed=embed, delete_after=5)

async def setup(bot):
    await bot.add_cog(RegistroCog(bot))