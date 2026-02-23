# Atributos Iniciais Base (o que todo mundo tem por padrão)
BASE_STATS = {
    "vida": 10, "energia": 10, "armadura": 5, "velocidade": 10,
    "soco": 1, "espada": 0, "arma": 0, "fruta": 0,
    "haki_armamento": 0, "haki_observacao": 0, "haki_rei": 0
}

# Modificadores por Facção
FACCOES = {
    "pirata": { # PIRATAS   
        
        #   VIDA = MEDIA, ENERGIA = NORMAL, ARMADURA = BAIXA, VELOCIDADE = ALTA 
        
        "vida" : 8,
        "vida_max": 8,
        "energia": 3,
        "energia_max": 3,
        "armadura": 2,
        "velocidade": 8,

    },
    "marine": { # MARINHA
        
        #   VIDA = ALTA, ENERGIA = NORMAL, ARMADURA = ALTA, VELOCIDADE = BAIXA 
        
        "vida" : 12,
        "vida_max": 12,
        "energia": 3,
        "energia_max": 3,
        "armadura": 5,
        "velocidade": 4,
    },
    "revolucionario": { # EXERCITO REVOLUCIONARIO
        
        #   VIDA = BAIXA, ENERGIA = NORMAL, ARMADURA = MUITO ALTA, VELOCIDADE = ALTA 
        
        "vida" : 6,
        "vida_max": 6,
        "energia": 3,
        "energia_max": 3,
        "armadura": 7,
        "velocidade": 8,
    },
    "cacador": { # CAÇADOR DE RECOMPENSAS
        
        #   VIDA = MEDIA, ENERGIA = NORMAL, ARMADURA = MEDIA, VELOCIDADE = MEDIA 
        
        "vida" : 7,
        "vida_max": 7,
        "energia": 3,
        "energia_max": 3,
        "armadura": 4,
        "velocidade": 5,
    }
}