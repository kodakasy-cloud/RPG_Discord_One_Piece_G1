from ui.cores import Cores

RACAS = {
    "humano": {
        "nome": "Humano",
        "emoji": "👤",
        "descricao": "A raça mais comum do mundo. Versáteis e adaptáveis.",
        "cor": Cores.CINZA_CLARO,
        "bonus": {"Sem bonus"},
        "historia": "Os humanos são encontrados em todos os mares. Sua força está na adaptabilidade e determinação."
    },
    
    "gigante": {
        "nome": "Gigante",
        "emoji": "🦍",
        "descricao": "Guerreiros enormes de Elbaf. Força bruta incomparável.",
        "cor": Cores.VERMELHO_FORTE,
        "bonus": {
            "vida": 5,
            "vida_max": 5,
            "armadura": 2,
            "soco": 3,
            "sorte": -2  # Gigantes são menos sortudos
        },
        "historia": "Originários da lendária ilha de Elbaf, os gigantes são guerreiros honrados que valorizam a força acima de tudo."
    },
    
    "tritao": {
        "nome": "Tritão",
        "emoji": "🧜‍♂️",
        "descricao": "Habitantes de Fish-Man Island. Mestres do combate aquático.",
        "cor": Cores.AZUL_FORTE,
        "bonus": {
            "vida": 2,
            "velocidade": 3,
            "soco": 2,
            "sorte": 2
        },
        "historia": "Seres que vivem nas profundezas do mar. Possuem força 10x maior que humanos quando na água."
    },
    
    "sereia": {
        "nome": "Sereia",
        "emoji": "🧜‍♀️",
        "descricao": "Seres místicos dos mares. Encantadoras e ágeis.",
        "cor": Cores.AZUL_CLARO,
        "bonus": {
            "velocidade": 3,
            "sorte": 8
        },
        "historia": "Conhecidas por sua beleza e canto hipnótico. Podem respirar debaixo d'água e se mover com graça incomparável."
    },
    
    "anjo": {
        "nome": "Anjo (Skypiean)",
        "emoji": "👼",
        "descricao": "Habitantes de Skypiea. Possuem asas e vivem nas nuvens.",
        "cor": Cores.BRANCO,
        "bonus": {
            "velocidade": 4,
            "sorte": 4
        },
        "historia": "Povo que vive no céu, nas ilhas de nuvens. Possuem pequenas asas nas costas e grande agilidade."
    },
    
    "minhokera": {
        "nome": "Minhokera (Longarm)",
        "emoji": "🦾",
        "descricao": "Tribo dos braços longos. Alcance superior em combate.",
        "cor": Cores.LARANJA_FORTE,
        "bonus": {
            "soco": 3,
            "espada": 2,
            "sorte": 1
        },
        "historia": "Possuem dois cotovelos em cada braço, permitindo golpes com alcance estendido e força incomum."
    },
    
    "perna_longuíssima": {
        "nome": "Perna Longa",
        "emoji": "🦵",
        "descricao": "Tribo das pernas longas. Chutes devastadores.",
        "cor": Cores.VERDE_CLARO,
        "bonus": {
            "velocidade": 4,
            "sorte": 2
        },
        "historia": "Pernas extraordinariamente longas que permitem velocidade superior e ataques poderosos."
    },
    
    "anão": {
        "nome": "Anão (Tontatta)",
        "emoji": "🪴",
        "descricao": "Pequenos guerreiros de Green Bit. Velozes e mortais.",
        "cor": Cores.VERDE_FORTE,
        "bonus": {
            "velocidade": 5,
            "sorte": 6
        },
        "historia": "Apesar do tamanho minúsculo, possuem velocidade impressionante e sorte incomum."
    },
    
    "lumarias": {
        "nome": "Lunaria",
        "emoji": "🔥",
        "descricao": "Tribo quase extinta. Poder do fogo nas costas.",
        "cor": Cores.VERMELHO_FORTE,
        "bonus": {
            "vida": 4,
            "vida_max": 4,
            "armadura": 3,
            "sorte": 3
        },
        "historia": "Raça lendária que podia criar chamas nas costas. Sobrevivem a qualquer condição extrema."
    },
    
    "three_eyes": {
        "nome": "Três Olhos",
        "emoji": "👁️👁️👁️",
        "descricao": "Tribo dos três olhos. Poderes mentais latentes.",
        "cor": Cores.ROXO_CLARO,
        "bonus": {
            "haki_observacao": 5,
            "sorte": 7
        },
        "historia": "Possuem um terceiro olho que, quando desperto, concede habilidades especiais como ler Poneglyphs."
    },
    
    "bucaneiro": {
        "nome": "Bucaneiro",
        "emoji": "🪨",
        "descricao": "Gigantes gentis. Força e coração gigantes.",
        "cor": Cores.MARROM,
        "bonus": {
            "vida": 6,
            "vida_max": 6,
            "armadura": 3,
            "sorte": 1
        },
        "historia": "Descendentes de gigantes que protegem os fracos. Conhecidos por sua bondade e força descomunal."
    }
}