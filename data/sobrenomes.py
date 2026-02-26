from ui.cores import Cores
import random

SOBRENOMES = {
    # ===== SEM SOBRENOME (sempre disponível como fallback) =====
    "None": {
        "nome": "Sem Sobrenome",
        "emoji": "❌",
        "raridade": "comum",
        "descricao": "Você ainda não possui um sobrenome de família.",
        "bonus": {},
        "historia": "Você carrega apenas seu próprio nome, livre para construir seu próprio legado."
    },
    
    # ===== COMUNS (40%) =====
    "Donquixote": {
        "nome": "Donquixote",
        "emoji": "👑",
        "raridade": "comum",
        "descricao": "Família nobre de descendência celestial.",
        "bonus": {
            "berries": 300,
        },
        "historia": "Uma das famílias mais poderosas do mundo. Conhecidos por sua ambição e influência."
    },
    
    # ===== RAROS (15%) =====
    
    "Garp": {
        "nome": "Garp",
        "emoji": "⚓",
        "raridade": "incomum",
        "descricao": "Família Garp. O herói da marinha.",
        "bonus": {
            "soco": 3,
            "vida": 5,
            "vida_max": 5
        },
        "historia": "A família do herói Monkey D. Garp. Punhos de ferro e coração de marinheiro."
    },
    
    # ===== ÉPICOS (10%) =====
    
    "Gol": {
        "nome": "Gol D.",
        "emoji": "💰",
        "raridade": "épico",
        "descricao": "Família do Rei dos Piratas.",
        "bonus": {
            "vida": 10,
            "vida_max": 10,
            "berries": 500,
        },
        "historia": "A família do lendário Gol D. Roger. Seu sangue carrega o destino dos reis."
    },
    
    # ===== LENDÁRIOS (6%) =====
    "Rocks": {
        "nome": "Rocks D.",
        "emoji": "😊",
        "raridade": "lendário",
        "descricao": "Século Vazio.",
        "bonus": {
            "vida": 25,
            "vida_max": 25,
            "armadura": 10,
        },
        "historia": "A figura lendária do Século Vazio.."
    },
    
    # ===== MÍTICOS (4%) =====
    "D": {
        "nome": "D.",
        "emoji": "⚡",
        "raridade": "mítico",
        "descricao": "Os portadores da vontade de D. Os inimigos naturais dos deuses.",
        "bonus": {
            "vida": 25,
            "vida_max": 25,
            "energia": 5,
            "soco": 10,
        },
        "historia": "Os portadores da vontade de D. Dizem que são os inimigos naturais dos deuses e carregam o destino do mundo."
    }
}

def sortear_sobrenome():
    """Sorteia um sobrenome baseado nas chances de raridade"""
    # Define as chances por raridade
    chances_raridade = {
        "comum": 40,
        "incomum": 30,
        "raro": 15,
        "épico": 10,
        "lendário": 4,
        "mítico": 1
    }
    
    # Primeiro, sorteia a raridade
    raridade_sorteada = random.choices(
        population=list(chances_raridade.keys()),
        weights=list(chances_raridade.values()),
        k=1
    )[0]
    
    # Depois, filtra os sobrenomes dessa raridade (excluindo "none")
    sobrenomes_da_raridade = [
        (key, sob) for key, sob in SOBRENOMES.items() 
        if sob['raridade'] == raridade_sorteada and key != 'none'
    ]
    
    # Se não houver sobrenomes dessa raridade, retorna "none"
    if not sobrenomes_da_raridade:
        return "none", SOBRENOMES["none"]
    
    # Sorteia um sobrenome específico dessa raridade
    sobrenome_sorteado = random.choice(sobrenomes_da_raridade)
    
    return sobrenome_sorteado[0], sobrenome_sorteado[1]