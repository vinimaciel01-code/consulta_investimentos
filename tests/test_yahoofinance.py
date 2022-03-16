import pandas as pd
from investimentos import ativos

dt1 = '01/01/2020'
dt2 = '31/12/2021'
lista_ativos = ['IRBR3.SA', 'HGBS11.SA']


def test_yahoocotacao():
    dados = ativos.yahoo_cotacao(lista_ativos, dt1, dt2)
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False


def test_yahoo_eventos():
    dados = ativos.yahoo_eventos(lista_ativos, dt1, dt2)
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False


def test_yahoo_dividendos():
    dados = ativos.yahoo_dividendos(lista_ativos, dt1, dt2)
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False
