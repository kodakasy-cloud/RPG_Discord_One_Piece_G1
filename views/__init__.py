# views/__init__.py
from .iniciar_view import IniciarView
from .select_faccao_view import FaccaoSelectView, mostrar_selecao_faccao
from .confirmacao_faccao_view import ConfirmacaoView

__all__ = ['IniciarView', 'FaccaoSelectView', 'ConfirmacaoView', 'mostrar_selecao_faccao']