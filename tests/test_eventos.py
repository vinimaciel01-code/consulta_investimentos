from consulta_investimentos.ativos_eventos import consulta_eventos


def test_eventos_ativos_retorna_nao_vazio():
    dados = consulta_eventos(['IRBR3.SA', 'HGBS11.SA', 'V', 'STOR'], '01/01/2020', '31/12/2021')
    assert dados.empty is False


def test_eventos_ativos_sem_fundo_retorna_nao_vazio():
    dados = consulta_eventos(['IRBR3.SA', 'V', 'STOR'], '01/01/2020', '31/12/2021')
    assert dados.empty is False


def test_eventos_ativos_apenas_fundo_retorna_nao_vazio():
    dados = consulta_eventos(['HGBS11.SA'], '01/01/2020', '31/12/2021')
    assert dados.empty is False


def test_eventos_lista_vazia_retorna_vazio():
    dados = consulta_eventos([], '01/01/2020', '31/12/2021')
    assert dados.empty


def test_eventos_data_inicio_vazia_retorna_vazio():
    dados = consulta_eventos(['V', 'STOR'], '', '31/12/2021')
    assert dados.empty


def test_eventos_data_fim_vazia_retorna_vazio():
    dados = consulta_eventos(['V', 'STOR'], '', '31/12/2021')
    assert dados.empty


def test_dividendos_data_fim_menor_que_dataa_inicio_retorna_vazio():
    dados = consulta_eventos(['V', 'STOR'], '01/03/2022', '31/12/2021')
    assert dados.empty is True
