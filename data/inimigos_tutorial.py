from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
IMAGEM_BANDIDO = BASE_DIR / "image" / "bandido_tutorial.png"

INIMIGO_TUTORIAL = {
    "nome": "Bandido",
    "descricao": "Um bandido qualquer, nem nome tem de tão insignificante!",
    "imagem_path": IMAGEM_BANDIDO, 
    "vida": 20,
    "vida_max": 20,
    "soco": 1,
    "defesa": 0,
    "velocidade": 0,
    "energia": 0,
    "energia_max": 10,
    "habilidades": {
        "basico": {
            "nome": "Golpe Sujo",
            "descricao": "Um golpe baixo, típico de bandido.",
            "dano": 1,
            "custo_energia": 0,
            "ganho_energia": 1
        },
        "especial": {
            "nome": "Facada Traiçoeira",
            "descricao": "Uma facada nas costas enquanto você não olha.",
            "dano": 3,
            "custo_energia": 3,
            "ganho_energia": 0
        }
    },
    "falas": {
        "inicio": "Parado! Eu vi esse dinheiro que você tem!",
        "turno": "Vai chorar?",
        "especial": "Morra!",
        "derrota": "Como... você... pode ser tão forte...",
        "vitoria": "Hahaha! Mais um otário derrotado!"
    }
}