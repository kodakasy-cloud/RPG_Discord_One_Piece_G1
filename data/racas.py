from ui.cores import Cores
import random

# Configurações de raridade
RARIDADES = {
    "comum": {"chance": 40, "cor": Cores.CINZA_CLARO, "emoji": "⬜", "nome": "COMUM"},
    "incomum": {"chance": 30, "cor": Cores.VERDE_CLARO, "emoji": "🟩", "nome": "INCOMUM"},
    "raro": {"chance": 15, "cor": Cores.AZUL_FORTE, "emoji": "🟦", "nome": "RARO"},
    "épico": {"chance": 10, "cor": Cores.ROXO_CLARO, "emoji": "🟪", "nome": "ÉPICO"},
    "lendário": {"chance": 4, "cor": Cores.DOURADO, "emoji": "🟨", "nome": "LENDÁRIO"},
    "mítico": {"chance": 1, "cor": Cores.VERMELHO_FORTE, "emoji": "🔴", "nome": "MÍTICO"}
}

RACAS = {
    # ===== COMUNS (40%) =====
    "humano": {
        "nome": "Humano",
        "emoji": "👤",
        "raridade": "comum",
        "descricao": "A raça mais comum do mundo. Versáteis e adaptáveis.",
        "bonus": {
            "soco": 1
        },
        "historia": "Os humanos são encontrados em todos os mares. Sua força está na adaptabilidade e determinação."
    },
    
    # ===== INCOMUNS (25%) =====
    "tritao": {
        "nome": "Tritão",
        "emoji": "🧜‍♂️",
        "raridade": "incomum",
        "descricao": "Habitantes de Fish-Man Island. Mestres do combate aquático.",
        "bonus": {
            "vida": 4,
            "soco": 3,
        },
        "historia": "Seres que vivem nas profundezas do mar. Possuem força 10x maior que humanos quando na água."
    },
    
    # ===== RAROS (15%) =====
    "gigante": {
        "nome": "Gigante",
        "emoji": "🦍",
        "raridade": "raro",
        "descricao": "Guerreiros enormes de Elbaf. Força bruta incomparável.",
        "bonus": {
            "vida": 10,
            "vida_max": 10,
            "armadura": 5,
            "soco": 6,
        },
        "historia": "Originários da lendária ilha de Elbaf, os gigantes são guerreiros honrados que valorizam a força acima de tudo."
    },
     
    # ===== ÉPICOS (10%) =====
    "anão": {
        "nome": "Anão (Tontatta)",
        "emoji": "🪴",
        "raridade": "épico",
        "descricao": "Pequenos guerreiros de Green Bit. Velozes e mortais.",
        "bonus": {
            "velocidade": 20,
        },
        "historia": "Apesar do tamanho minúsculo, possuem velocidade impressionante e sorte incomum."
    },  
    # ===== LENDÁRIOS (6%) =====
    "lumarias": {
        "nome": "Lunaria",
        "emoji": "🔥",
        "raridade": "lendário",
        "descricao": "Tribo quase extinta. Poder do fogo nas costas.",
        "bonus": {
            "vida": 8,
            "vida_max": 8,
            "armadura": 6,
        },
        "historia": "Raça lendária que podia criar chamas nas costas. Sobrevivem a qualquer condição extrema."
    },
    
    # ===== MÍTICOS (4%) =====
    "king": {
        "nome": "Rei",
        "emoji": "👑🔥",
        "raridade": "mítico",
        "descricao": "Poder supremo.",
        "bonus": {
            "vida": 15,
            "vida_max": 15,
            "armadura": 5,
            "velocidade": 10,
            "soco": 5,
            "espada": 5,
            "arma": 5,
            "fruta": 5
        },
        "historia": "????"
    },

}

def sortear_raca():
    """Sorteia uma raça baseada nas chances de raridade"""
    # Primeiro, sorteia a raridade
    raridade_sorteada = random.choices(
        population=list(RARIDADES.keys()),
        weights=[r['chance'] for r in RARIDADES.values()],
        k=1
    )[0]
    
    # Depois, filtra as raças dessa raridade
    racas_da_raridade = [
        (key, raca) for key, raca in RACAS.items() 
        if raca['raridade'] == raridade_sorteada
    ]
    
    # Sorteia uma raça específica dessa raridade
    raca_sorteada = random.choice(racas_da_raridade)
    
    return raca_sorteada[0], raca_sorteada[1]