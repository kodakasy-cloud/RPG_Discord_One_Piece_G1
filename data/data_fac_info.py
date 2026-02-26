# Atributos Iniciais Base (o que todo mundo tem por padrão)
BASE_STATS = {
    "vida": 10, 
    "vida_max": 10,
    "energia": 10,
    "energia_max":10, 
    "armadura": 5, 
    "velocidade": 10,
    "soco": 1, 
    "espada": 0, 
    "arma": 0, 
    "fruta": 0,
    "haki_armamento": 0, 
    "haki_observacao": 0, 
    "haki_rei": 0
}

# Modificadores por Facção
FACCOES = {
    "pirata": {  # PIRATAS - VIDA MÉDIA, VELOCIDADE ALTA
        "vida": 10,
        "vida_max": 10,
        "energia": 10,
        "energia_max": 10,
        "armadura": 1,
        "velocidade": 5,
    },
    "marine": {  # MARINHA - VIDA ALTA, ARMADURA ALTA
        "vida": 17,
        "vida_max": 17,
        "energia": 5,
        "energia_max": 5,
        "armadura": 4,
        "velocidade": 3,
    },
    "revolucionario": {  # REVOLUCIONÁRIOS - ARMADURA MUITO ALTA
        "vida": 8,
        "vida_max": 8,
        "energia": 7,
        "energia_max": 7,
        "armadura": 9,
        "velocidade": 9,
    },
    "cacador": {  # CAÇADORES - EQUILIBRADO
        "vida": 12,
        "vida_max": 12,
        "energia": 7,
        "energia_max": 7,
        "armadura": 3,
        "velocidade": 6,
    }
}