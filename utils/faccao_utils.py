# utils/faccao_utils.py
from data.data_fac_info import FACCOES

def get_stats_faccao(faccao: str) -> dict:
    return FACCOES.get(faccao, {}).copy()


def formatar_stats_para_embed(stats: dict) -> str:
    """
    Formata os stats para exibição em embed
    Retorna algo como: "❤️ 8 | 🛡️ 2 | ⚡ 8"
    """
    return (
        f"❤️ {stats.get('vida', 0)} | "
        f"🛡️ {stats.get('armadura', 0)} | "
        f"⚡ {stats.get('velocidade', 0)}"
    )


def calcular_vida_maxima(stats: dict) -> int:
    """Calcula a vida máxima considerando bônus"""
    return stats.get('vida_max', stats.get('vida', 0))


def calcular_energia_maxima(stats: dict) -> int:
    """Calcula a energia máxima considerando bônus"""
    return stats.get('energia_max', stats.get('energia', 0))