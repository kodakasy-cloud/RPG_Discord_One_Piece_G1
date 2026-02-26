import discord
from discord.ui import View, Button
from database.connection import SessionLocal
from models.usuario import Usuario
from models.jogador import Jogador
from ui.cores import Cores
from data.data_fac_info import BASE_STATS, FACCOES
from data.inimigos_tutorial import INIMIGO_TUTORIAL
from views.batalha_tutorial_view import BatalhaTutorialView
import asyncio

# Importação corrigida - não importar IniciarTutorialView daqui
# from cogs.tutorial_combate import IniciarTutorialView

class ConfirmacaoView(View):
    def __init__(self, user_id, nome_usuario, faccao, raca_info, sobrenome_info):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.nome_usuario = nome_usuario
        self.faccao = faccao
        self.raca_info = raca_info
        self.sobrenome_info = sobrenome_info
        self.mensagem = None
        
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ Esta confirmação não é para você!", ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="✅ CONFIRMAR", style=discord.ButtonStyle.success)
    async def confirmar(self, interaction: discord.Interaction, button: Button):
        await self.criar_personagem(interaction)
    
    @discord.ui.button(label="❌ CANCELAR", style=discord.ButtonStyle.danger)
    async def cancelar(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="❌ **REGISTRO CANCELADO**",
            description="Use `!registrar` quando quiser tentar novamente.",
            color=Cores.VERMELHO_FORTE
        )
        
        for item in self.children:
            item.disabled = True
            
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def criar_personagem(self, interaction: discord.Interaction):
        """Cria o personagem no banco de dados e inicia o tutorial"""
        
        db = SessionLocal()
        try:
            # Verifica se já existe usuário
            usuario = db.query(Usuario).filter_by(
                discord_id=str(self.user_id)
            ).first()
            
            if usuario:
                embed = discord.Embed(
                    title="❌ **ERRO**",
                    description="Você já possui um personagem!",
                    color=Cores.VERMELHO_FORTE
                )
                await interaction.response.edit_message(embed=embed, view=None)
                return
            
            # Cria novo usuário
            usuario = Usuario(
                discord_id=str(self.user_id),
                nome_discord=interaction.user.name,
                data_registro=discord.utils.utcnow()
            )
            db.add(usuario)
            db.flush()
            
            # ===== CÁLCULO DOS STATUS =====
            stats_finais = BASE_STATS.copy()
            
            # Soma stats da facção
            stats_faccao = FACCOES.get(self.faccao, {})
            for stat, valor in stats_faccao.items():
                stats_finais[stat] = stats_finais.get(stat, 0) + valor
            
            # Soma bônus da raça
            bonus_raca = self.raca_info['info'].get('bonus', {})
            for stat, valor in bonus_raca.items():
                stats_finais[stat] = stats_finais.get(stat, 0) + valor
            
            # Soma bônus do sobrenome
            if self.sobrenome_info['key'] != 'none':
                bonus_sobrenome = self.sobrenome_info['info'].get('bonus', {})
                for stat, valor in bonus_sobrenome.items():
                    stats_finais[stat] = stats_finais.get(stat, 0) + valor
            
            # Cria o jogador
            from data.faccao_config import FACCAO_INFO
            
            novo_jogador = Jogador(
                usuario_id=usuario.id,
                nome=interaction.user.name,
                faccao=self.faccao,
                raca=self.raca_info["key"],
                sobrenome=self.sobrenome_info["key"] if self.sobrenome_info["key"] != 'none' else None,
                nivel=1,
                xp=0,
                xp_next=10,
                berries=stats_finais.get('berries', 50),
                vida=stats_finais.get('vida', 10),
                vida_max=stats_finais.get('vida', 10),
                energia=stats_finais.get('energia', 0),
                energia_max=stats_finais.get('energia_max', 10),
                armadura=stats_finais.get('armadura', 0),
                velocidade=stats_finais.get('velocidade', 10),
                soco=stats_finais.get('soco', 1),
                espada=stats_finais.get('espada', 0),
                arma=stats_finais.get('arma', 0),
                fruta=stats_finais.get('fruta', 0),
                haki_armamento=stats_finais.get('haki_armamento', 0),
                haki_observacao=stats_finais.get('haki_observacao', 0),
                haki_rei=stats_finais.get('haki_rei', 0),
                vitorias=0,
                derrotas=0
            )
            
            db.add(novo_jogador)
            db.commit()
            
            # ===== CRIA UM DICIONÁRIO COM OS DADOS DO JOGADOR =====
            jogador_data = {
                "vida": novo_jogador.vida,
                "vida_max": novo_jogador.vida_max,
                "soco": novo_jogador.soco,
                "nome": novo_jogador.nome,
                "berries": novo_jogador.berries,
                "xp": novo_jogador.xp
            }
            
            # ===== PERSONAGEM CRIADO COM SUCESSO =====
            embed_sucesso = discord.Embed(
                title="✅ **PERSONAGEM CRIADO!**",
                description=f"### Bem-vindo, {interaction.user.name}!",
                color=Cores.VERDE_CLARO
            )
            
            embed_sucesso.add_field(
                name="📋 **SEU PERSONAGEM**",
                value=(
                    f"**Raça:** {self.raca_info['info']['nome']}\n"
                    f"**Sobrenome:** {self.sobrenome_info['info']['nome']}\n"
                    f"**Facção:** {FACCAO_INFO[self.faccao]['nome']}"
                ),
                inline=False
            )
            
            embed_sucesso.set_footer(text="Preparando tutorial...")
            
            for item in self.children:
                item.disabled = True
                
            await interaction.response.edit_message(embed=embed_sucesso, view=self)
            
            # ===== AGUARDA 2 SEGUNDOS E INICIA O TUTORIAL =====
            await asyncio.sleep(2)
            
            # ===== INICIA O TUTORIAL NA MESMA MENSAGEM =====
            from cogs.tutorial_combate import TutorialCombateCog
            
            # Cria cópia do inimigo
            inimigo = INIMIGO_TUTORIAL.copy()
            inimigo["vida"] = inimigo["vida_max"]
            
            # ===== TELA DE TUTORIAL - INSTRUÇÕES =====
            embed_tutorial = discord.Embed(
                title="⚔️ **TUTORIAL DE COMBATE** ⚔️",
                description=f"Bem-vindo, **{interaction.user.name}**!",
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
            
            embed_tutorial.add_field(
                name="📚 **COMO JOGAR**",
                value=instrucoes,
                inline=False
            )
            
            embed_tutorial.set_footer(text="Clique no botão abaixo para enfrentar o desafio!")
            
            # Pega o cog de tutorial
            tutorial_cog = interaction.client.get_cog('TutorialCombateCog')
            
            if not tutorial_cog:
                # Se não encontrar o cog, cria uma instância básica
                from cogs.tutorial_combate import TutorialCombateCog
                tutorial_cog = TutorialCombateCog(interaction.client)
            
            # Adiciona o usuário aos tutoriais ativos
            tutorial_cog.tutoriais_ativos[self.user_id] = True
            
            # Importa a classe IniciarTutorialView dentro da função para evitar importação circular
            from cogs.tutorial_combate import IniciarTutorialView
            
            # Botão para começar
            view_tutorial = IniciarTutorialView(
                self.user_id, 
                novo_jogador,  # Passa o objeto jogador
                inimigo, 
                interaction.client, 
                tutorial_cog,
                jogador_data  # Passa também o dicionário com os dados
            )
            
            # Envia a mensagem do tutorial na MESMA mensagem
            await interaction.message.edit(embed=embed_tutorial, view=view_tutorial)
            view_tutorial.mensagem = interaction.message
            
        except Exception as e:
            print(f"Erro ao criar personagem: {e}")
            db.rollback()
            
            embed_erro = discord.Embed(
                title="❌ **ERRO**",
                description=f"Ocorreu um erro: ```{str(e)}```",
                color=Cores.VERMELHO_FORTE
            )
            
            try:
                await interaction.followup.send(embed=embed_erro, ephemeral=True)
            except:
                pass
        finally:
            db.close()