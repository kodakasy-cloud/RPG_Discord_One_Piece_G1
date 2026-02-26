# dados_ilha.py - Informações das ilhas

ILHAS = {
    "inicial": {
        "nome": "Fosha Vilage",
        "descricao": "Uma pequena ilha pacífica, perfeita para começar sua jornada. A brisa do mar traz cheiro de aventura e os habitantes locais são amigáveis.",
        "imagem": "https://i.imgur.com/Za5vrCr.jpeg",  # Substitua pela URL da sua imagem
        "procurados": [
            {"nome": "Bandido da Praia", "recompensa": 500, "nivel": 1},
            {"nome": "Ladrão do Porto", "recompensa": 300, "nivel": 1}
        ]
    },
    "porto": {
        "nome": "Porto Comercial",
        "descricao": "Um movimentado porto cheio de comerciantes e marinheiros. O cheiro de peixe fresco e especiarias enche o ar.",
        "imagem": "https://i.imgur.com/QbJPIum.jpeg",
        "procurados": [
            {"nome": "Contrabandista", "recompensa": 800, "nivel": 2}
        ]
    }
}

# Imagem padrão caso não encontre
IMAGEM_PADRAO = "https://i.imgur.com/ExemploPadrao.png"