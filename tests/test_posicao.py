# import pandas as pd
# from consulta_investimentos.ativos_posicao.posicao import consulta_posicao
#
# dt1 = '01/01/2020'
# dt2 = '31/12/2021'
# lista_ativos = ['IRBR3.SA', 'HGBS11.SA']
#
#
# def test_posicao_retorna_nao_vazio():
#     dados = consulta_posicao(lista_ativos, dt1, dt2)
#     if isinstance(dados, pd.DataFrame):
#         assert dados.empty is False
#     else:
#         assert False
