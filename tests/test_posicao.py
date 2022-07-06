import pandas as pd

from consulta_investimentos.ativos_posicao.posicao import consulta_posicao
import tests.config as config

dt1 = '01/01/2020'
dt2 = '31/12/2021'

def test_posicao_retorna_nao_vazio():
    dados = consulta_posicao(config.path_download, dt1, dt2)
    if isinstance(dados, pd.DataFrame):
        assert dados.empty is False
    else:
        assert False
