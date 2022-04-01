from consulta_investimentos.ativos_dividendos import consulta_dividendos


def test_dividendos_ativos_retorna_nao_vazio():
    dados = consulta_dividendos(['IRBR3.SA', 'HGBS11.SA', 'V', 'STOR'], '01/01/2020', '31/12/2021')
    assert dados.empty is False


def test_dividendos_ativos_sem_fundo_retorna_nao_vazio():
    dados = consulta_dividendos(['IRBR3.SA', 'V', 'STOR'], '01/01/2020', '31/12/2021')
    assert dados.empty is False


def test_dividendos_ativos_apenas_fundo_retorna_nao_vazio():
    dados = consulta_dividendos(['HGBS11.SA'], '01/01/2020', '31/12/2021')
    assert dados.empty is False


def test_dividendos_lista_vazia_retorna_vazio():
    dados = consulta_dividendos([], '01/01/2020', '31/12/2021')
    assert dados.empty


def test_dividendos_data_inicio_vazia_retorna_vazio():
    dados = consulta_dividendos(['V', 'STOR'], '', '31/12/2021')
    assert dados.empty


def test_dividendos_data_fim_vazia_retorna_vazio():
    dados = consulta_dividendos(['V', 'STOR'], '', '31/12/2021')
    assert dados.empty


def test_dividendos_data_fim_menor_que_dataa_inicio_retorna_vazio():
    dados = consulta_dividendos(['V', 'STOR'], '01/03/2022', '31/12/2021')
    assert dados.empty is True
