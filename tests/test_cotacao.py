from consulta_investimentos.ativos_cotacoes import consulta_cotacoes


def test_cotacoes_dois_ativos_retorna_nao_vazio():
    dados = consulta_cotacoes(['IRBR3.SA', 'HGBS11.SA', 'V', 'STOR'], '01/01/2020', '31/12/2021')
    assert dados.empty is False


def test_cotacoes_lista_vazia_retorna_vazio():
    dados = consulta_cotacoes([], '01/01/2020', '31/12/2021')
    assert dados.empty


def test_cotacoes_data_inicio_vazia_retorna_vazio():
    dados = consulta_cotacoes(['V', 'STOR'], '', '31/12/2021')
    assert dados.empty


def test_cotacoes_data_fim_vazia_retorna_vazio():
    dados = consulta_cotacoes(['V', 'STOR'], '', '31/12/2021')
    assert dados.empty


def test_cotacoes_data_fim_menor_que_dataa_inicio_retorna_vazio():
    dados = consulta_cotacoes(['V', 'STOR'], '01/03/2022', '31/12/2021')
    assert dados.empty is True
