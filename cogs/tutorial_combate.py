import discord
from discord.ext import commands
from ui.cores import Cores
from data.inimigos_tutorial import INIMIGO_TUTORIAL
from views.batalha_tutorial_view import BatalhaTutorialView
import asyncio
import random

class IniciarTutorialView(discord.ui.View):
    def __init__(self, user_id, jogador, inimigo, bot, cog, jogador_data=None):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.jogador = jogador
        self.inimigo = inimigo
        self.bot = bot
        self.cog = cog
        self.mensagem = None
        
        # ===== SOLUÇÃO: Usa o dicionário se fornecido, senão cria um =====
        if jogador_data:
            self.jogador_data = jogador_data
        else:
            # Cria um dicionário com os dados necessários
            self.jogador_data = {
                "vida": jogador.vida,
                "vida_max": jogador.vida_max,
                "soco": jogador.soco,
                "nome": jogador.nome,
                "berries": jogador.berries,
                "xp": jogador.xp
            }
    
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
        
        # Guarda referência do cog na view de batalha
        view.cog = self.cog
        
        # Embed inicial do combate - USANDO OS DADOS DO DICIONÁRIO
        embed_combate = discord.Embed(
            title=f"⚔️ **{self.inimigo['nome'].upper()}** ⚔️",
            description=f"*{self.inimigo['descricao']}*",
            color=Cores.AZUL_FORTE
        )
        
        # Status do jogador - USANDO O DICIONÁRIO
        jogador_info = (
            f"💪 **SAUDÁVEL**\n"
            f"\n**VIDA**\n{view.criar_barra_vida(self.jogador_data['vida'], self.jogador_data['vida_max'])}\n"
            f"\n**ENERGIA**\n⚡ {'⚪' * 3} `0/3`\n"
            f"\n👊 **DANO** `{self.jogador_data['soco']}`"
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


class TutorialCombateCog(commands.Cog):
    def __init__(self, bot):  # ← APENAS O BOT, sem outros parâmetros
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
        from database.connection import SessionLocal
        from models.usuario import Usuario
        from models.jogador import Jogador
        
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
    
    async def voltar_ao_perfil(self, interaction, jogador):
        """Função para voltar ao perfil com botões"""
        
        from database.connection import SessionLocal
        from models.usuario import Usuario
        from models.jogador import Jogador
        from data.faccao_config import FACCAO_INFO
        from views.perfil_menu_view import PerfilMenuView
        
        db = SessionLocal()
        try:
            usuario = db.query(Usuario).filter_by(
                discord_id=str(interaction.user.id)
            ).first()
            
            if not usuario or not jogador:
                return
            
            # Busca o jogador atualizado no banco
            jogador_atualizado = db.query(Jogador).filter_by(id=jogador.id).first()
            
            # Recria o embed do perfil
            info_faccao = FACCAO_INFO.get(jogador_atualizado.faccao, {})
            
            embed_perfil = discord.Embed(
                title=f"⚔️ **PERFIL DE {interaction.user.name.upper()}** ⚔️",
                color=info_faccao.get('cor', Cores.AZUL_FORTE)
            )
            
            embed_perfil.set_thumbnail(url=interaction.user.display_avatar.url)
            
            # Raça e Sobrenome
            raca_text = getattr(jogador_atualizado, 'raca', None) or "Nenhuma"
            sobrenome_text = getattr(jogador_atualizado, 'sobrenome', None) or "Nenhum"
            
            info_basica = (
                f"**Facção:** {info_faccao.get('emoji', '')} {info_faccao.get('nome', 'Desconhecida')}\n"
                f"**Nível:** {jogador_atualizado.nivel}\n"
                f"**XP:** {jogador_atualizado.xp}\n"
                f"**Berries:** 💰 {jogador_atualizado.berries}\n"
                f"**Raça:** {raca_text}\n"
                f"**Sobrenome:** {sobrenome_text}\n"
                f"**Registro:** {usuario.data_registro.strftime('%d/%m/%Y')}"
            )
            embed_perfil.add_field(name="📋 **INFORMAÇÕES**", value=info_basica, inline=False)
            
            status_combate = (
                f"❤️ **Vida:** {jogador_atualizado.vida}/{jogador_atualizado.vida_max}\n"
                f"🛡️ **Armadura:** {jogador_atualizado.armadura}\n"
                f"🏃 **Velocidade:** {jogador_atualizado.velocidade}\n"
                f"⚔️ **Vitórias:** {jogador_atualizado.vitorias}\n"
                f"💔 **Derrotas:** {jogador_atualizado.derrotas}"
            )
            embed_perfil.add_field(name="⚔️ **COMBATE**", value=status_combate, inline=True)
            
            estilos = (
                f"👊 **Soco:** {jogador_atualizado.soco}\n"
                f"⚔️ **Espada:** {jogador_atualizado.espada}\n"
                f"🔫 **Arma:** {jogador_atualizado.arma}\n"
                f"🍎 **Fruta:** {jogador_atualizado.fruta}"
            )
            embed_perfil.add_field(name="🥋 **HABILIDADES**", value=estilos, inline=True)
            
            hakis = (
                f"🛡️ **Armamento:** {jogador_atualizado.haki_armamento}\n"
                f"👁️ **Observação:** {jogador_atualizado.haki_observacao}\n"
                f"👑 **Rei:** {jogador_atualizado.haki_rei}"
            )
            embed_perfil.add_field(name="🌀 **HAKIS**", value=hakis, inline=True)
            
            xp_proximo = jogador_atualizado.nivel * 100
            xp_atual = jogador_atualizado.xp
            percentual = min(100, int((xp_atual / xp_proximo) * 100))
            barra = "🟩" * (percentual // 10) + "⬜" * (10 - (percentual // 10))
            
            embed_perfil.add_field(
                name="📊 **PROGRESSÃO**",
                value=f"**Nível {jogador_atualizado.nivel}**\n{barra} {percentual}%\n`{xp_atual}/{xp_proximo} XP`",
                inline=False
            )
            
            embed_perfil.set_footer(text=f"ID: {jogador_atualizado.id} • Use o menu abaixo para navegar")
            
            # CRIA A VIEW DO PERFIL COM BOTÕES
            view_perfil = PerfilMenuView(interaction.user.id, jogador_atualizado, self.bot)
            
            # EDITA a mensagem atual para mostrar o perfil com botões
            if interaction:
                await interaction.message.edit(embed=embed_perfil, view=view_perfil, attachments=[])
            
        except Exception as e:
            print(f"Erro ao voltar ao perfil: {e}")
        finally:
            db.close()


async def setup(bot):
    await bot.add_cog(TutorialCombateCog(bot))  # ← Passa apenas o bot