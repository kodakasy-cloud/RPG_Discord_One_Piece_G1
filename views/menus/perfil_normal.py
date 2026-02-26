import discord
from ui.cores import Cores
from data.faccao_config import FACCAO_INFO
from database.connection import SessionLocal
from models.usuario import Usuario
from models.jogador import Jogador
from views.buttons.menu_principal import *

async def show_perfil_normal(view, interaction: discord.Interaction):
    """Mostra o perfil normal com todas as informações e botões principais"""
    
    db = SessionLocal()
    try:
        # Busca os dados atualizados do jogador
        usuario = db.query(Usuario).filter_by(
            discord_id=str(view.user_id)
        ).first()
        
        if not usuario:
            await interaction.followup.send("❌ Usuário não encontrado!", ephemeral=True)
            return
        
        jogador = db.query(Jogador).filter_by(usuario_id=usuario.id).first()
        if not jogador:
            await interaction.followup.send("❌ Jogador não encontrado!", ephemeral=True)
            return
        
        info_faccao = FACCAO_INFO.get(jogador.faccao, {})
        
        embed = discord.Embed(
            title=f"⚔️ **{interaction.user.name}**",
            color=info_faccao.get('cor', Cores.AZUL_FORTE)
        )
        
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        
        raca_text = getattr(jogador, 'raca', None) or "Nenhuma"
        sobrenome_text = getattr(jogador, 'sobrenome', None) or "Nenhum"
        
        # CABEÇALHO
        embed.add_field(name="", value=f"⚔️ {interaction.user.name} • 📜 {sobrenome_text}", inline=False)
        embed.add_field(name="", value=f"{info_faccao.get('emoji', '')} {info_faccao.get('nome', '???')} • 🧬 {raca_text}", inline=False)
        embed.add_field(name="", value="━" * 40, inline=False)
        
        # VIDA E ENERGIA
        barra_vida = view.criar_barra_vida(jogador.vida, jogador.vida_max)
        barra_energia = view.criar_barra_energia(jogador.energia, jogador.energia_max)
        embed.add_field(name="", value=f"❤️ {barra_vida} {jogador.vida}/{jogador.vida_max}  ⚡ {barra_energia} {jogador.energia}/{jogador.energia_max}", inline=False)
        embed.add_field(name="", value="━" * 40, inline=False)
        
        # STATUS E HABILIDADES
        embed.add_field(name="", value="⚔️ STATUS", inline=False)
        embed.add_field(name="", value=f"🛡️ Armadura: {jogador.armadura}  👊 Soco: {jogador.soco} • ⚔️ Espada: {jogador.espada}", inline=False)
        embed.add_field(name="", value=f"🏃 Velocidade: {jogador.velocidade} • 🍎 Fruta: {jogador.fruta} • 🔫 Arma: {jogador.arma}", inline=False)
        embed.add_field(name="", value="━" * 40, inline=False)
        
        # VITÓRIAS E DERROTAS
        embed.add_field(name="", value=f"⚔️ Vitórias: {jogador.vitorias}  💔 Derrotas: {jogador.derrotas}", inline=False)
        embed.add_field(name="", value="━" * 40, inline=False)
        
        # PROGRESSÃO
        xp_proximo = jogador.nivel * 100
        embed.add_field(name="", value=f"💰 B$ {jogador.berries} • NÍVEL {jogador.nivel}", inline=False)
        embed.add_field(name="", value=f"{view.criar_barra_xp(jogador.xp, xp_proximo)} {jogador.xp}/{xp_proximo} XP", inline=False)
        embed.add_field(name="", value="━" * 40, inline=False)
        
        # ID e Data
        embed.add_field(name="", value=f"ID: {jogador.id} • Update v0.5 • {usuario.data_registro.strftime('%d/%m/%Y')}", inline=False)
        
        # Recria a view com os botões principais
        view.clear_items()
        view.add_item(IlhaButton(view.user_id, jogador, view.bot, view))
        view.add_item(NavegarButton(view.user_id, jogador, view.bot))
        view.add_item(InventarioButton(view.user_id, jogador, view.bot, view))
        view.add_item(ConfigButton(view.user_id, jogador, view.bot))
        view.add_item(SairButton(view.user_id, jogador, view.bot))
        
        await interaction.response.edit_message(embed=embed, view=view)
        
    except Exception as e:
        print(f"Erro ao mostrar perfil: {e}")
    finally:
        db.close()