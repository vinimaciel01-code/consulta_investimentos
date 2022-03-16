import pandas as pd
from investimentos import cotacoes_moeda

valor = 1
origem = 'USD'
destino = 'BRL'


def test_cotacoes_moeda():
    dados = cotacoes_moeda.get_rates(1, 'USD', 'BRL')
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False


if __name__ == '__main__':
    test_cotacoes_moeda()
