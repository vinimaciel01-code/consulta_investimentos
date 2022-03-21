import pandas as pd
from investimentos.ativos_eventos.eventos import consulta_eventos

dt1 = '01/01/2020'
dt2 = '31/12/2021'


def test_eventos_retorna_nao_vazio_uma_acao():
    lista_ativos = ['ABEV3.SA']
    dados = consulta_eventos(lista_ativos, dt1, dt2)
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False


def test_eventos_retorna_nao_vazio_mais_uma_acao():
    lista_ativos = ['ABEV3.SA', 'EGIE3.SA']
    dados = consulta_eventos(lista_ativos, dt1, dt2)
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False


def test_eventos_retorna_nao_vazio_um_fundo():
    lista_ativos = ['HGBS11.SA']
    dados = consulta_eventos(lista_ativos, dt1, dt2)
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False


def test_eventos_retorna_nao_vazio_mais_um_fundo():
    lista_ativos = ['HGBS11.SA', 'HGRE11.SA']
    dados = consulta_eventos(lista_ativos, dt1, dt2)
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False


def test_eventos_retorna_nao_vazio_um_acao_fundo():
    lista_ativos = ['ABEV3.SA', 'HGBS11.SA']
    dados = consulta_eventos(lista_ativos, dt1, dt2)
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False


def test_eventos_retorna_nao_vazio_mais_um_acao_fundo():
    lista_ativos = ['ABEV3.SA', 'EGIE3.SA', 'HGBS11.SA', 'HGRE11.SA']
    dados = consulta_eventos(lista_ativos, dt1, dt2)
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False