import pandas as pd
from investimentos.moeda_cotacao.moedas import consulta_moedas

valor = 1
origem = 'USD'
destino = 'BRL'


def test_cotacoesmoeda_retorna_nao_vazio():
    """Testa cotações de moedas."""
    dados = consulta_moedas(1, 'USD', 'BRL')
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False
