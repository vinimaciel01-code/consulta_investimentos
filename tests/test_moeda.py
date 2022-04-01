import pytest
from consulta_investimentos.moeda_cotacao.moedas import consulta_moedas


def test_moeda_retorna_nao_vazio():
    dados = consulta_moedas('USD', 'BRL')
    assert dados.empty is not True


@pytest.mark.xfail
def test_moeda_base_vazia_retorna_erro():
    consulta_moedas('', 'BRL')


@pytest.mark.xfail
def test_moeda_destino_vazia_retorna_erro():
    consulta_moedas('USD', '')


@pytest.mark.xfail
def test_moedas_vazias_retorna_erro():
    consulta_moedas('USD', 'BRL')


def test_moeda_usd_para_brl_em_data_especifica_retorna_valor_especifico():
    dados = consulta_moedas('USD', 'BRL', dt1='01/01/2022')
    assert dados["1USD:BRL"][0] == 5.570577


def test_moeda_usd_para_brl_2_em_data_especifica_retorna_valor_especifico():
    dados = consulta_moedas('USD', 'BRL', valor=2, dt1='01/01/2022')
    assert dados["2USD:BRL"][0] == 11.141154
