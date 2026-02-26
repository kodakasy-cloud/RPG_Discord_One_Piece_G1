import discord
import asyncio
import random
from ui.cores import Cores
from pathlib import Path

class BatalhaTutorialView(discord.ui.View):
    def __init__(self, user_id, jogador, inimigo, bot):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.jogador = jogador
        self.inimigo = inimigo
        self.bot = bot
        self.turno_atual = "jogador"
        self.energia_jogador = 0
        self.energia_inimigo = 0
        self.desviando = False
        self.caminho_imagem = None
        self.mensagem_combate = None
        
        # Carrega a imagem
        if 'imagem_path' in inimigo:
            self.caminho_imagem = Path(inimigo['imagem_path'])
            if self.caminho_imagem.exists():
                print(f"[OK] Imagem carregada: {self.caminho_imagem}")
    
    def get_arquivo_imagem(self):
        """Cria um novo arquivo de imagem a cada chamada"""
        if self.caminho_imagem and self.caminho_imagem.exists():
            return discord.File(self.caminho_imagem, filename="bandido.png")
        return None
    
    def criar_barra_vida(self, vida_atual, vida_maxima, tamanho=6):
        """Cria uma barra de vida visual baseada na porcentagem"""
        percentual = (vida_atual / vida_maxima) * 100
        blocos_cheios = int((percentual / 100) * tamanho)
        
        # Escolhe a cor baseada na porcentagem
        if percentual > 60:
            cor = "🟩"
        elif percentual > 30:
            cor = "🟨"
        else:
            cor = "🟥"
        
        barra = cor * blocos_cheios + "⬛" * (tamanho - blocos_cheios)
        return f"{barra} `{vida_atual}/{vida_maxima}`"
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Verifica se é o usuário correto"""
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Esta não é sua batalha!", ephemeral=True)
            return False
        return True
    
    async def atualizar_embed(self, interaction: discord.Interaction, mensagem_acao: str = ""):
        """Atualiza o embed com status atual da batalha"""
        
        # Status de vida do jogador
        percent_jogador = (self.jogador.vida / self.jogador.vida_max) * 100
        if percent_jogador > 50:
            status_vida = "💪 **SAUDÁVEL**"
        elif percent_jogador > 20:
            status_vida = "⚠️ **FERIDO**"
        else:
            status_vida = "💀 **MORRENDO**"
        
        # Barras de vida
        barra_vida_jogador = self.criar_barra_vida(self.jogador.vida, self.jogador.vida_max)
        barra_vida_inimigo = self.criar_barra_vida(self.inimigo["vida"], self.inimigo["vida_max"])
        
        # Energia visual
        energia_jogador = "🔵" * self.energia_jogador + "⚪" * (3 - self.energia_jogador)
        energia_inimigo = "🔴" * self.energia_inimigo + "⚪" * (3 - self.energia_inimigo)
        
        # JOGADOR
        jogador_info = (
            f"{status_vida}\n"
            f"\n**VIDA**\n{barra_vida_jogador}\n"
            f"\n**ENERGIA**\n⚡ {energia_jogador} `{self.energia_jogador}/3`\n"
            f"\n👊 **DANO** `{self.jogador.soco}`"
        )
        
        # INIMIGO
        inimigo_info = (
            f"EM ALERTA! \n"
            f"\n**VIDA**\n{barra_vida_inimigo}\n"
            f"\n**ENERGIA**\n⚡ {energia_inimigo} `{self.energia_inimigo}/3`\n"
            f"\n👊 **DANO** `{self.inimigo['soco']}`"
        )
        
        # Embed principal
        embed = discord.Embed(
            title=f"⚔️",
            description=f"*{self.inimigo['descricao']}*",
            color=Cores.AZUL_FORTE
        )
        
        # Imagem (se houver)
        arquivo_imagem = self.get_arquivo_imagem()
        if arquivo_imagem:
            embed.set_thumbnail(url="attachment://bandido.png")
        
        # VS no meio
        embed.add_field(name="👤 **JOGADOR**", value=jogador_info, inline=True)
        embed.add_field(name="⚔️ ", value="\u200b\n\u200b\n⚔️\n\u200b\n\u200b", inline=True)
        embed.add_field(name="👾 **INIMIGO**", value=inimigo_info, inline=True)
        
        # Linha separadora
        embed.add_field(name="\u200b", value="━━━━━━━━━━━━━━━━━━━━━━", inline=False)
        
        # Mensagem de ação
        if mensagem_acao:
            embed.add_field(name="📢 **AÇÃO**", value=mensagem_acao, inline=False)
        
        # Fala do inimigo (se for turno dele)
        if self.turno_atual == "inimigo" and not mensagem_acao:
            embed.add_field(
                name="👾 **FALA**", 
                value=f"*{self.inimigo['falas']['turno']}*", 
                inline=False
            )
        
        # Linha separadora
        embed.add_field(name="\u200b", value="━━━━━━━━━━━━━━━━━━━━━━", inline=False)
        
        # Turno
        if self.turno_atual == "jogador":
            embed.add_field(name="🎮 **SEU TURNO!**", value="Escolha uma ação abaixo.", inline=False)
        else:
            embed.add_field(name="⏳ **AGUARDE**", value="Turno do inimigo...", inline=False)
        
        # Tempo restante
        embed.set_footer(text="⏰ 120 segundos para agir")
        
        # Atualiza a mensagem
        try:
            if self.mensagem_combate:
                if arquivo_imagem:
                    await self.mensagem_combate.edit(embed=embed, view=self, attachments=[arquivo_imagem])
                else:
                    await self.mensagem_combate.edit(embed=embed, view=self)
        except Exception as e:
            print(f"Erro ao atualizar embed: {e}")
    
    @discord.ui.button(label="👊 SOCO FORTE", style=discord.ButtonStyle.primary, emoji="⚡", row=0)
    async def soco_forte(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.turno_atual != "jogador":
            await interaction.response.send_message("⏳ Aguarde seu turno!", ephemeral=True)
            return
        
        if not self.mensagem_combate:
            await interaction.response.send_message("❌ Erro: mensagem de combate não encontrada!", ephemeral=True)
            return
        
        await interaction.response.defer()
        
        for item in self.children:
            item.disabled = True
        await self.mensagem_combate.edit(view=self)
        
        dano_base = self.jogador.soco
        variacao = random.randint(-1, 1)
        dano_final = max(1, dano_base + variacao)
        
        self.inimigo["vida"] = max(0, self.inimigo["vida"] - dano_final)
        self.energia_jogador = min(3, self.energia_jogador + 1)
        
        if dano_final > dano_base:
            emoji_dano = "💥 CRÍTICO!"
        elif dano_final < dano_base:
            emoji_dano = "👎 FRACO..."
        else:
            emoji_dano = "👊 NORMAL"
        
        mensagem = f"**{emoji_dano}** Você causou **{dano_final}** de dano! (+1⚡)"
        
        await self.atualizar_embed(interaction, mensagem)
        
        if self.inimigo["vida"] <= 0:
            await self.finalizar_batalha(interaction, vitoria=True)
            return
        
        self.turno_atual = "inimigo"
        await asyncio.sleep(1.5)
        await self.turno_inimigo(interaction)
        
        for item in self.children:
            item.disabled = False
        await self.mensagem_combate.edit(view=self)
    
    @discord.ui.button(label="💥 PUNHO DE RAIVA", style=discord.ButtonStyle.danger, emoji="💢", row=0)
    async def punho_raiva(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.turno_atual != "jogador":
            await interaction.response.send_message("⏳ Aguarde seu turno!", ephemeral=True)
            return
        
        if not self.mensagem_combate:
            await interaction.response.send_message("❌ Erro: mensagem de combate não encontrada!", ephemeral=True)
            return
        
        if self.energia_jogador < 3:
            await interaction.response.send_message(
                f"❌ Energia insuficiente! Você tem {self.energia_jogador}/3.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        for item in self.children:
            item.disabled = True
        await self.mensagem_combate.edit(view=self)
        
        multiplicador = random.randint(3, 5)
        dano_base = self.jogador.soco * multiplicador
        variacao = random.randint(-2, 2)
        dano_final = max(5, dano_base + variacao)
        
        self.inimigo["vida"] = max(0, self.inimigo["vida"] - dano_final)
        self.energia_jogador = 0
        
        if multiplicador == 5:
            destaque = "🔥 **MÁXIMO PODER!** 🔥"
        elif multiplicador == 4:
            destaque = "⚡ **MUITO FORTE!** ⚡"
        else:
            destaque = "💢 **PODEROSO!** 💢"
        
        mensagem = f"{destaque} {multiplicador}x dano! Você causou **{dano_final}** de dano!"
        
        await self.atualizar_embed(interaction, mensagem)
        
        if self.inimigo["vida"] <= 0:
            await self.finalizar_batalha(interaction, vitoria=True)
            return
        
        self.turno_atual = "inimigo"
        await asyncio.sleep(1.5)
        await self.turno_inimigo(interaction)
        
        for item in self.children:
            item.disabled = False
        await self.mensagem_combate.edit(view=self)
    
    @discord.ui.button(label="🛡️ DESVIAR", style=discord.ButtonStyle.secondary, emoji="💨", row=0)
    async def desviar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.turno_atual != "jogador":
            await interaction.response.send_message("⏳ Aguarde seu turno!", ephemeral=True)
            return
        
        if not self.mensagem_combate:
            await interaction.response.send_message("❌ Erro: mensagem de combate não encontrada!", ephemeral=True)
            return
        
        await interaction.response.defer()
        
        for item in self.children:
            item.disabled = True
        await self.mensagem_combate.edit(view=self)
        
        mensagem = "💨 **Posição defensiva ativada!** 50% de chance de esquivar e ganhar 3⚡"
        
        await self.atualizar_embed(interaction, mensagem)
        
        self.turno_atual = "inimigo"
        self.desviando = True
        await asyncio.sleep(1.5)
        await self.turno_inimigo(interaction)
        
        for item in self.children:
            item.disabled = False
        await self.mensagem_combate.edit(view=self)
    
    # ===== MÉTODO TURNO_INIMIGO ADICIONADO =====
    async def turno_inimigo(self, interaction: discord.Interaction):
        """Processa o turno do inimigo"""
        
        await self.atualizar_embed(interaction, f"👾 **{self.inimigo['nome']}** vai atacar...")
        await asyncio.sleep(1.5)
        
        # Salva estado do desvio
        estava_desviando = self.desviando
        self.desviando = False
        
        # Inimigo decide qual ataque usar
        if self.energia_inimigo >= 3:
            dano = self.inimigo["habilidades"]["especial"]["dano"]
            nome_ataque = self.inimigo['habilidades']['especial']['nome']
            mensagem = f"💢 **{nome_ataque}!** O inimigo causa **{dano}** de dano!"
            self.energia_inimigo = 0
        else:
            dano = self.inimigo["habilidades"]["basico"]["dano"]
            nome_ataque = self.inimigo['habilidades']['basico']['nome']
            mensagem = f"👊 **{nome_ataque}!** O inimigo causa **{dano}** de dano!"
            self.energia_inimigo = min(3, self.energia_inimigo + 1)
        
        # Verifica desvio
        if estava_desviando:
            chance_esquiva = 0.5
            if random.random() < chance_esquiva:
                self.energia_jogador = 3
                mensagem += f"\n\n✨ **DESVIO PERFEITO!** Você esquivou e ganhou 3⚡!"
                dano = 0
            else:
                mensagem += f"\n\n⚠️ **Desvio falhou...**"
        
        # Aplica dano no jogador
        self.jogador.vida = max(0, self.jogador.vida - dano)
        
        await self.atualizar_embed(interaction, mensagem)
        
        # Verifica se jogador morreu
        if self.jogador.vida <= 0:
            await self.finalizar_batalha(interaction, vitoria=False)
            return
        
        # Volta turno para o jogador
        self.turno_atual = "jogador"
        await asyncio.sleep(1.5)
        await self.atualizar_embed(interaction, "✅ **SEU TURNO!**")
    
    async def finalizar_batalha(self, interaction: discord.Interaction, vitoria: bool):
        """Finaliza a batalha com resultado"""
        
        if vitoria:
            # Calcula estatísticas
            dano_total = self.inimigo["vida_max"] - self.inimigo["vida"]
            turnos = 3  # Você pode calcular isso se quiser
            
            # ===== TELA DE VITÓRIA INICIAL =====
            embed = discord.Embed(
                title="🏆 **VITÓRIA!** 🏆",
                description=f"Parabéns! Você derrotou **{self.inimigo['nome']}**!",
                color=Cores.VERDE_CLARO
            )
            
            # Últimas palavras do inimigo
            embed.add_field(
                name="💀 **ÚLTIMAS PALAVRAS**",
                value=f"*{self.inimigo['falas']['derrota']}*",
                inline=False
            )
            
            # Mini resumo da batalha
            resumo = (
                f"```\n"
                f"📊  RESUMO DA BATALHA  📊\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"💥 Dano total: {dano_total}\n"
                f"⚡ Energia final: {self.energia_jogador}/3\n"
                f"🔄 Turnos: {turnos}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"```"
            )
            embed.add_field(name="📋 **RESUMO**", value=resumo, inline=False)
            
            # Recompensas
            embed.add_field(
                name="🎁 **RECOMPENSAS**",
                value="```\nNenhuma recompensa no momento\n```",
                inline=False
            )
            
            # Desabilita botões
            for item in self.children:
                item.disabled = True
            
            # Atualiza para a tela de vitória
            await self.mensagem_combate.edit(embed=embed, view=self, attachments=[])
            
            # ===== CONTAGEM REGRESSIVA DE 5 SEGUNDOS =====
            for i in range(5, 0, -1):
                embed_countdown = discord.Embed(
                    title="🏆 **VITÓRIA!** 🏆",
                    description=f"Parabéns! Você derrotou **{self.inimigo['nome']}**!",
                    color=Cores.VERDE_CLARO
                )
                
                embed_countdown.add_field(
                    name="💀 **ÚLTIMAS PALAVRAS**", 
                    value=f"*{self.inimigo['falas']['derrota']}*", 
                    inline=False
                )
                embed_countdown.add_field(
                    name="📋 **RESUMO**", 
                    value=resumo, 
                    inline=False
                )
                embed_countdown.add_field(
                    name="🎁 **RECOMPENSAS**", 
                    value="```\nNenhuma recompensa no momento\n```", 
                    inline=False
                )
                embed_countdown.add_field(
                    name="⏳ **REDIRECIONANDO**", 
                    value=f"Redirecionando para o perfil em **{i}**...", 
                    inline=False
                )
                embed_countdown.set_footer(text="Prepare-se para ver seus status!")
                
                await self.mensagem_combate.edit(embed=embed_countdown, view=self)
                await asyncio.sleep(1)
            
            # ===== BUSCA OS DADOS DO JOGADOR PARA O PERFIL =====
            from database.connection import SessionLocal
            from models.usuario import Usuario
            from models.jogador import Jogador
            from data.faccao_config import FACCAO_INFO
            from views.perfil_menu_view import PerfilMenuView  # <-- IMPORTANTE: Importar a view do perfil
            
            db = SessionLocal()
            try:
                # Busca o usuário e jogador atualizados
                usuario = db.query(Usuario).filter_by(discord_id=str(interaction.user.id)).first()
                jogador = db.query(Jogador).filter_by(usuario_id=usuario.id).first() if usuario else None
                
                if jogador:
                    # Pega informações da facção
                    info_faccao = FACCAO_INFO.get(jogador.faccao, {})
                    
                    # ===== CRIA O EMBED DO PERFIL =====
                    embed_perfil = discord.Embed(
                        title=f"⚔️ **PERFIL DE {interaction.user.name.upper()}** ⚔️",
                        color=info_faccao.get('cor', Cores.AZUL_FORTE)
                    )
                    
                    # Thumbnail com avatar
                    embed_perfil.set_thumbnail(url=interaction.user.display_avatar.url)
                    
                    # Informações básicas
                    info_basica = (
                        f"**Facção:** {info_faccao.get('emoji', '')} {info_faccao.get('nome', 'Desconhecida')}\n"
                        f"**Nível:** {jogador.nivel}\n"
                        f"**XP:** {jogador.xp}\n"
                        f"**Berries:** 💰 {jogador.berries}\n"
                    )
                    embed_perfil.add_field(name="📋 **INFORMAÇÕES**", value=info_basica, inline=False)
                    
                    # Status de combate
                    status_combate = (
                        f"❤️ **Vida:** {jogador.vida}/{jogador.vida_max}\n"
                        f"🛡️ **Armadura:** {jogador.armadura}\n"
                        f"🏃 **Velocidade:** {jogador.velocidade}\n"
                        f"⚔️ **Vitórias:** {jogador.vitorias}\n"
                        f"💔 **Derrotas:** {jogador.derrotas}"
                    )
                    embed_perfil.add_field(name="⚔️ **COMBATE**", value=status_combate, inline=True)
                    
                    # Estilos de luta
                    estilos = (
                        f"👊 **Soco:** {jogador.soco}\n"
                        f"⚔️ **Espada:** {jogador.espada}\n"
                        f"🔫 **Arma:** {jogador.arma}\n"
                        f"🍎 **Fruta:** {jogador.fruta}"
                    )
                    embed_perfil.add_field(name="🥋 **HABILIDADES**", value=estilos, inline=True)
                    
                    # Hakis
                    hakis = (
                        f"🛡️ **Armamento:** {jogador.haki_armamento}\n"
                        f"👁️ **Observação:** {jogador.haki_observacao}\n"
                        f"👑 **Rei:** {jogador.haki_rei}"
                    )
                    embed_perfil.add_field(name="🌀 **HAKIS**", value=hakis, inline=True)
                    
                    # Barra de XP
                    xp_proximo = jogador.nivel * 100
                    xp_atual = jogador.xp
                    percentual = min(100, int((xp_atual / xp_proximo) * 100))
                    barra = "🟩" * (percentual // 10) + "⬜" * (10 - (percentual // 10))
                    
                    embed_perfil.add_field(
                        name="📊 **PROGRESSÃO**",
                        value=f"**Nível {jogador.nivel}**\n{barra} {percentual}%\n`{xp_atual}/{xp_proximo} XP`",
                        inline=False
                    )
                    
                    # Footer
                    embed_perfil.set_footer(text="Use !perfil para ver novamente")
                    
                    # ===== CRIA A VIEW DO PERFIL COM BOTÕES =====
                    view_perfil = PerfilMenuView(interaction.user.id, jogador, self.bot)
                    
                    # ===== ATUALIZA A MESMA MENSAGEM PARA O PERFIL COM BOTÕES =====
                    await self.mensagem_combate.edit(embed=embed_perfil, view=view_perfil, attachments=[])
                else:
                    # Fallback se não encontrar o jogador
                    embed_fallback = discord.Embed(
                        title="✅ **REDIRECIONADO**",
                        description="Use `!perfil` para ver seus status!",
                        color=Cores.AZUL_FORTE
                    )
                    await self.mensagem_combate.edit(embed=embed_fallback, view=None, attachments=[])
                    
            except Exception as e:
                print(f"Erro ao carregar perfil: {e}")
                embed_erro = discord.Embed(
                    title="❌ **ERRO**",
                    description=f"Use `!perfil` manualmente.",
                    color=Cores.VERMELHO_FORTE
                )
                await self.mensagem_combate.edit(embed=embed_erro, view=None, attachments=[])
            finally:
                db.close()
        
        else:
            # Tela de derrota (mantida igual)
            embed = discord.Embed(
                title="💀 **DERROTA** 💀",
                description=f"Você foi derrotado por **{self.inimigo['nome']}**...",
                color=Cores.VERMELHO_FORTE
            )
            
            embed.add_field(
                name="👾 **GRITO DE VITÓRIA**",
                value=f"*{self.inimigo['falas']['vitoria']}*",
                inline=False
            )
            
            embed.add_field(
                name="📚 **DICAS**",
                value="```\nUse DESVIO para ganhar energia\nAcumule 3⚡ para usar PUNHO DE RAIVA\n```",
                inline=False
            )
            
            embed.set_footer(text="Tente novamente quando estiver pronto!")
            
            for item in self.children:
                item.disabled = True
            
            await self.mensagem_combate.edit(embed=embed, view=self, attachments=[])


async def setup(bot):
    pass