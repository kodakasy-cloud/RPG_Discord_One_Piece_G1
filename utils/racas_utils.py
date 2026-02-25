from data.racas import RACAS, RARIDADES, sortear_raca
from data.sobrenomes import SOBRENOMES, sortear_sobrenome

def get_bonus_raca(raca: str) -> dict:
    """Retorna os bônus da raça escolhida"""
    return RACAS.get(raca, RACAS["humano"]).get("bonus", {})

def get_bonus_sobrenome(sobrenome: str) -> dict:
    """Retorna os bônus do sobrenome escolhido"""
    return SOBRENOMES.get(sobrenome, SOBRENOMES["none"]).get("bonus", {})

def aplicar_bonus_ao_jogador(jogador, raca: str, sobrenome: str):
    """Aplica todos os bônus de raça e sobrenome ao jogador"""
    bonus_raca = get_bonus_raca(raca)
    bonus_sobrenome = get_bonus_sobrenome(sobrenome)
    
    # Combina todos os bônus
    todos_bonus = {**bonus_raca, **bonus_sobrenome}
    
    # Aplica cada bônus ao jogador
    for atributo, valor in todos_bonus.items():
        if hasattr(jogador, atributo):
            atual = getattr(jogador, atributo)
            setattr(jogador, atributo, atual + valor)
    
    return jogador

def get_info_raca(raca: str) -> dict:
    """Retorna informações completas da raça"""
    return RACAS.get(raca, RACAS["humano"])

def get_info_sobrenome(sobrenome: str) -> dict:
    """Retorna informações completas do sobrenome"""
    return SOBRENOMES.get(sobrenome, SOBRENOMES["none"])

def sortear_raca_e_sobrenome():
    """Sorteia uma raça e um sobrenome com suas respectivas chances"""
    raca_key, raca_info = sortear_raca()
    sobrenome_key, sobrenome_info = sortear_sobrenome()
    
    return {
        "raca": {"key": raca_key, "info": raca_info},
        "sobrenome": {"key": sobrenome_key, "info": sobrenome_info}
    }

def resumo_raridades() -> str:
    """Gera um resumo das chances por raridade"""
    resumo = "**📊 PROBABILIDADES**\nChances de cada raridade:\n\n"
    
    ordem = ["comum", "incomum", "raro", "épico", "lendário", "mítico"]
    
    for raridade in ordem:
        config = RARIDADES[raridade]
        resumo += f"{config['emoji']} **{config['nome']}**\n`{config['chance']}%`"
        
        if raridade != "mítico":
            resumo += "\n\n"
    
    return resumo

def resumo_probabilidades() -> str:
    """Gera um resumo completo das probabilidades com quantidades"""
    resumo = "**📊 PROBABILIDADES**\nChances de cada raridade:\n\n"
    
    ordem = ["comum", "incomum", "raro", "épico", "lendário", "mítico"]
    
    for raridade in ordem:
        config = RARIDADES[raridade]
        
        # Conta quantidades
        qtd_racas = len([r for r in RACAS.values() if r['raridade'] == raridade])
        qtd_sobres = len([s for s in SOBRENOMES.values() if s['raridade'] == raridade and s['nome'] != "Sem Sobrenome"])
        
        resumo += f"{config['emoji']} **{config['nome']}**\n"
        resumo += f"`{config['chance']}%` • {qtd_racas} raças • {qtd_sobres} sobrenomes\n\n"
    
    return resumo

def resumo_racas() -> str:
    """Gera um resumo organizado de todas as raças"""
    resumo = "**📋 RAÇAS DISPONÍVEIS**\n\n"
    
    ordem = ["comum", "incomum", "raro", "épico", "lendário", "mítico"]
    
    for raridade in ordem:
        racas_da_raridade = [(key, raca) for key, raca in RACAS.items() if raca['raridade'] == raridade]
        
        if racas_da_raridade:
            config = RARIDADES[raridade]
            resumo += f"{config['emoji']} **{config['nome']}**\n"
            
            for key, raca in racas_da_raridade:
                bonus = " • ".join([f"+{v} {k}" for k, v in raca['bonus'].items()])
                resumo += f"{raca['emoji']} **{raca['nome']}**: {bonus}\n"
            
            resumo += "\n"
    
    total_racas = len(RACAS)
    resumo += f"**Total: {total_racas} raças**"
    
    return resumo

def resumo_sobrenomes() -> str:
    """Gera um resumo organizado de todos os sobrenomes (sem incluir 'none')"""
    resumo = "**📋 SOBRENOMES DISPONÍVEIS**\n\n"
    
    ordem = ["incomum", "raro", "épico", "lendário", "mítico"]
    
    # Filtra apenas sobrenomes que não são "none"
    sobrenomes_filtrados = {key: sob for key, sob in SOBRENOMES.items() if key != 'none'}
    
    for raridade in ordem:
        sobrenomes_da_raridade = [(key, sob) for key, sob in sobrenomes_filtrados.items() 
                                  if sob['raridade'] == raridade]
        
        if sobrenomes_da_raridade:
            config = RARIDADES.get(raridade, {"emoji": "⬜", "nome": raridade.upper()})
            resumo += f"{config['emoji']} **{config['nome']}**\n"
            
            for key, sob in sobrenomes_da_raridade:
                bonus = " • ".join([f"+{v} {k}" for k, v in sob['bonus'].items()])
                resumo += f"{sob['emoji']} **{sob['nome']}**: {bonus}\n"
            
            resumo += "\n"
    
    total_sobrenomes = len([s for s in SOBRENOMES.values() if s['nome'] != "Sem Sobrenome"])
    resumo += f"**Total: {total_sobrenomes} sobrenomes**"
    
    return resumo