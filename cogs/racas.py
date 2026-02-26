import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
from utils.racas_utils import (
    sortear_raca_e_sobrenome,
    resumo_racas,
    resumo_sobrenomes,
    resumo_probabilidades
)
from data.racas import RACAS, RARIDADES
from data.sobrenomes import SOBRENOMES
from ui.cores import Cores

class RacasView(View):
    def __init__(self, ctx, bot):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.bot = bot
        self.message = None
        self.rolagem_ativa = False
        
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if self.message:
            try:
                await self.message.edit(view=self)
            except:
                pass
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("❌ Apenas quem usou o comando pode interagir!", ephemeral=True)
            return False
        return True

    async def menu_racas(self, interaction: discord.Interaction):
        """Função auxiliar para mostrar o menu de raças"""
        embed = discord.Embed(
            title="🏴‍☠️ SISTEMA DE RAÇAS",
            description="Escolha uma opção abaixo:",
            color=Cores.DOURADO
        )
        
        embed.add_field(
            name="**COMANDOS**",
            value=(
                "**Linha 1** • 🎲 Sortear Raça | 📋 Lista Raças\n"
                "**Linha 2** • 📜 Sortear Sobrenome | 📋 Lista Sobrenomes\n"
                "**Linha 3** • ⭐ Sortear Ambos | 📊 Chances | 🏠 Menu"
            ),
            inline=False
        )
        
        embed.set_footer(text=f"Solicitado por {interaction.user.name}")
        
        # Reativa todos os botões
        for item in self.children:
            item.disabled = False
            
        await interaction.edit_original_response(embed=embed, view=self)

    # ===== LINHA 1 =====
    @discord.ui.button(label="🎲 SORTEAR RAÇA", style=discord.ButtonStyle.primary, row=0)
    async def sortear_raca_button(self, interaction: discord.Interaction, button: Button):
        if self.rolagem_ativa:
            await interaction.response.send_message("⏳ Uma rolagem já está em andamento!", ephemeral=True)
            return
        
        self.rolagem_ativa = True
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        
        try:
            from data.racas import sortear_raca
            raca_key, raca_info = sortear_raca()
            
            embed_descricao = discord.Embed(
                description=f"**Descrição:**\n{raca_info['descricao']}",
                color=RARIDADES[raca_info['raridade']]['cor']
            )
            embed_descricao.set_footer(text="🤔 Qual será? Revelando em 3 segundos...")
            
            await interaction.edit_original_response(embed=embed_descricao)
            await asyncio.sleep(3)
            
            bonus = ", ".join([f"+{v} {k}" for k, v in raca_info['bonus'].items()]) or "Nenhum bônus"
            
            embed_resultado = discord.Embed(
                title=f"{raca_info['emoji']} RAÇA SORTEADA",
                description=f"Parabéns {self.ctx.author.mention}!",
                color=RARIDADES[raca_info['raridade']]['cor']
            )
            
            embed_resultado.add_field(
                name=f"**{raca_info['nome']}**",
                value=(
                    f"**Raridade:** {RARIDADES[raca_info['raridade']]['emoji']} {raca_info['raridade'].upper()}\n"
                    f"**Bônus:** {bonus}\n"
                    f"**Descrição:** {raca_info['descricao']}"
                ),
                inline=False
            )
            
            embed_resultado.add_field(
                name="📖 História",
                value=raca_info['historia'],
                inline=False
            )
            
            for item in self.children:
                item.disabled = False
            await interaction.edit_original_response(embed=embed_resultado, view=self)
            
        finally:
            self.rolagem_ativa = False

    @discord.ui.button(label="📋 LISTA RAÇAS", style=discord.ButtonStyle.secondary, row=0)
    async def lista_racas_button(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="📋 RAÇAS DISPONÍVEIS",
            description=resumo_racas(),
            color=Cores.AZUL_FORTE
        )
        await interaction.response.edit_message(embed=embed, view=self)

    # ===== LINHA 2 =====
    @discord.ui.button(label="📜 SORTEAR SOBRENOME", style=discord.ButtonStyle.success, row=1)
    async def sortear_sobrenome_button(self, interaction: discord.Interaction, button: Button):
        if self.rolagem_ativa:
            await interaction.response.send_message("⏳ Uma rolagem já está em andamento!", ephemeral=True)
            return
        
        self.rolagem_ativa = True
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        
        try:
            from data.sobrenomes import sortear_sobrenome
            sobrenome_key, sobrenome_info = sortear_sobrenome()
            
            cor = RARIDADES[sobrenome_info['raridade']]['cor'] if sobrenome_info['raridade'] in RARIDADES else Cores.ROXO_CLARO
            
            embed_descricao = discord.Embed(
                description=f"**Descrição:**\n{sobrenome_info['descricao']}",
                color=cor
            )
            embed_descricao.set_footer(text="🤔 Qual será? Revelando em 3 segundos...")
            
            await interaction.edit_original_response(embed=embed_descricao)
            await asyncio.sleep(3)
            
            bonus = ", ".join([f"+{v} {k}" for k, v in sobrenome_info['bonus'].items()]) or "Nenhum bônus"
            
            embed_resultado = discord.Embed(
                title=f"{sobrenome_info['emoji']} SOBRENOME SORTEADO",
                description=f"Parabéns {self.ctx.author.mention}!",
                color=cor
            )
            
            embed_resultado.add_field(
                name=f"**{sobrenome_info['nome']}**",
                value=(
                    f"**Raridade:** {RARIDADES.get(sobrenome_info['raridade'], {'emoji': '⬜'})['emoji']} {sobrenome_info['raridade'].upper()}\n"
                    f"**Bônus:** {bonus}\n"
                    f"**Descrição:** {sobrenome_info['descricao']}"
                ),
                inline=False
            )
            
            if sobrenome_key != 'none':
                embed_resultado.add_field(
                    name="📖 História",
                    value=sobrenome_info['historia'],
                    inline=False
                )
            
            for item in self.children:
                item.disabled = False
            await interaction.edit_original_response(embed=embed_resultado, view=self)
            
        finally:
            self.rolagem_ativa = False

    @discord.ui.button(label="📋 LISTA SOBRENOMES", style=discord.ButtonStyle.secondary, row=1)
    async def lista_sobrenomes_button(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="📋 SOBRENOMES DISPONÍVEIS",
            description=resumo_sobrenomes(),
            color=Cores.ROXO_CLARO
        )
        await interaction.response.edit_message(embed=embed, view=self)

    # ===== LINHA 3 =====
    @discord.ui.button(label="⭐ SORTEAR AMBOS", style=discord.ButtonStyle.danger, row=2)
    async def sortear_ambos_button(self, interaction: discord.Interaction, button: Button):
        if self.rolagem_ativa:
            await interaction.response.send_message("⏳ Uma rolagem já está em andamento!", ephemeral=True)
            return
        
        self.rolagem_ativa = True
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)
        
        try:
            resultado = sortear_raca_e_sobrenome()
            raca = resultado["raca"]["info"]
            sobrenome = resultado["sobrenome"]["info"]
            
            embed_descricao = discord.Embed(color=Cores.DOURADO)
            embed_descricao.add_field(
                name="🎲 RAÇA",
                value=f"**Descrição:** {raca['descricao']}",
                inline=False
            )
            embed_descricao.add_field(
                name="📜 SOBRENOME",
                value=f"**Descrição:** {sobrenome['descricao']}",
                inline=False
            )
            embed_descricao.set_footer(text="🤔 Quais serão? Revelando em 3 segundos...")
            
            await interaction.edit_original_response(embed=embed_descricao)
            await asyncio.sleep(3)
            
            bonus_raca = ", ".join([f"+{v} {k}" for k, v in raca['bonus'].items()]) or "Nenhum"
            bonus_sobrenome = ", ".join([f"+{v} {k}" for k, v in sobrenome['bonus'].items()]) or "Nenhum"
            
            todos_bonus = {**raca['bonus'], **sobrenome['bonus']}
            total = ", ".join([f"+{v} {k}" for k, v in todos_bonus.items()]) if todos_bonus else "Nenhum bônus"
            
            embed_resultado = discord.Embed(
                title="⭐ SORTEIO COMPLETO",
                description=f"Parabéns {self.ctx.author.mention}!",
                color=Cores.DOURADO
            )
            
            embed_resultado.add_field(
                name=f"{raca['emoji']} Raça: {raca['nome']}",
                value=f"{RARIDADES[raca['raridade']]['emoji']} {raca['raridade']}\n➕ {bonus_raca}",
                inline=True
            )
            embed_resultado.add_field(
                name=f"{sobrenome['emoji']} Sobrenome: {sobrenome['nome']}",
                value=f"{RARIDADES.get(sobrenome['raridade'], {'emoji': '⬜'})['emoji']} {sobrenome['raridade']}\n➕ {bonus_sobrenome}",
                inline=True
            )
            embed_resultado.add_field(
                name="📊 Total de Bônus",
                value=total,
                inline=False
            )
            
            for item in self.children:
                item.disabled = False
            await interaction.edit_original_response(embed=embed_resultado, view=self)
            
        finally:
            self.rolagem_ativa = False

    @discord.ui.button(label="📊 CHANCES", style=discord.ButtonStyle.secondary, row=2)
    async def chances_button(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="📊 PROBABILIDADES",
            description=resumo_probabilidades(),
            color=Cores.DOURADO
        )
        await interaction.response.edit_message(embed=embed, view=self)

@discord.ui.button(label="🏠 MENU", style=discord.ButtonStyle.success, row=2)
async def menu_principal_button(self, interaction: discord.Interaction, button: Button):
    """Volta para o perfil do jogador (versão atualizada)"""
    
    for item in self.children:
        item.disabled = True
    await interaction.response.edit_message(view=self)
    
    try:
        # Busca os dados atualizados do jogador
        from database.connection import SessionLocal
        from models.usuario import Usuario
        from models.jogador import Jogador
        
        db = SessionLocal()
        try:
            usuario = db.query(Usuario).filter_by(
                discord_id=str(interaction.user.id)
            ).first()
            
            if usuario:
                jogador = db.query(Jogador).filter_by(usuario_id=usuario.id).first()
                
                if jogador:
                    # Cria um contexto falso para executar o comando !perfil
                    ctx = await self.bot.get_context(interaction.message)
                    ctx.author = interaction.user
                    
                    # Pega o cog de perfil e chama o comando diretamente
                    perfil_cog = self.bot.get_cog('PerfilCog')
                    
                    if perfil_cog:
                        # Chama o comando perfil que vai mostrar a versão ATUALIZADA
                        await perfil_cog.perfil(ctx)
                        return
        finally:
            db.close()
        
        # Se não conseguir, volta para o menu de raças
        await self.menu_racas(interaction)
            
    except Exception as e:
        print(f"Erro ao voltar para o perfil: {e}")
        await self.menu_racas(interaction)

class Racas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="racas", aliases=["raças"], invoke_without_command=True)
    async def racas(self, ctx):
        """Menu principal do sistema de raças"""
        
        embed = discord.Embed(
            title="🏴‍☠️ SISTEMA DE RAÇAS",
            description="Escolha uma opção abaixo:",
            color=Cores.DOURADO
        )
        
        embed.add_field(
            name="**COMANDOS**",
            value=(
                "**Linha 1** • 🎲 Sortear Raça | 📋 Lista Raças\n"
                "**Linha 2** • 📜 Sortear Sobrenome | 📋 Lista Sobrenomes\n"
                "**Linha 3** • ⭐ Sortear Ambos | 📊 Chances | 🏠 Menu"
            ),
            inline=False
        )
        
        embed.set_footer(text=f"Solicitado por {ctx.author.name}")
        
        view = RacasView(ctx, self.bot)
        view.message = await ctx.send(embed=embed, view=view)

    async def mostrar_menu_racas(self, interaction: discord.Interaction, ctx):
        """Mostra o menu de raças editando a mensagem atual (chamado pelo perfil)"""
        
        embed = discord.Embed(
            title="🏴‍☠️ SISTEMA DE RAÇAS",
            description="Escolha uma opção abaixo:",
            color=Cores.DOURADO
        )
        
        embed.add_field(
            name="**COMANDOS**",
            value=(
                "**Linha 1** • 🎲 Sortear Raça | 📋 Lista Raças\n"
                "**Linha 2** • 📜 Sortear Sobrenome | 📋 Lista Sobrenomes\n"
                "**Linha 3** • ⭐ Sortear Ambos | 📊 Chances | 🏠 Menu"
            ),
            inline=False
        )
        
        embed.set_footer(text=f"Solicitado por {ctx.author.name}")
        
        view = RacasView(ctx, self.bot)
        await interaction.edit_original_response(embed=embed, view=view)

    @racas.command(name="info")
    async def info_raca_sobrenome(self, ctx, *, nome: str):
        """Mostra informações detalhadas de uma raça ou sobrenome"""
        nome = nome.lower().strip()
        
        for key, raca in RACAS.items():
            if key == nome or raca['nome'].lower() == nome:
                bonus = ", ".join([f"+{v} {k}" for k, v in raca['bonus'].items()]) or "Nenhum"
                
                embed = discord.Embed(
                    title=f"{raca['emoji']} {raca['nome']}",
                    description=raca['descricao'],
                    color=RARIDADES[raca['raridade']]['cor']
                )
                embed.add_field(name="Raridade", value=f"{RARIDADES[raca['raridade']]['emoji']} {raca['raridade'].upper()}", inline=True)
                embed.add_field(name="Bônus", value=bonus, inline=True)
                embed.add_field(name="História", value=raca['historia'], inline=False)
                
                await ctx.send(embed=embed)
                return
        
        for key, sob in SOBRENOMES.items():
            if key == nome or sob['nome'].lower() == nome:
                bonus = ", ".join([f"+{v} {k}" for k, v in sob['bonus'].items()]) or "Nenhum"
                
                cor = RARIDADES[sob['raridade']]['cor'] if sob['raridade'] in RARIDADES else Cores.CINZA_CLARO
                
                embed = discord.Embed(
                    title=f"{sob['emoji']} {sob['nome']}",
                    description=sob['descricao'],
                    color=cor
                )
                
                raridade_text = f"{RARIDADES.get(sob['raridade'], {'emoji': '⬜'})['emoji']} {sob['raridade'].upper()}"
                embed.add_field(name="Raridade", value=raridade_text, inline=True)
                embed.add_field(name="Bônus", value=bonus, inline=True)
                
                if key != 'none':
                    embed.add_field(name="História", value=sob['historia'], inline=False)
                
                await ctx.send(embed=embed)
                return
        
        await ctx.send(f"❌ Nada encontrado com o nome: **{nome}**")

async def setup(bot):
    await bot.add_cog(Racas(bot))