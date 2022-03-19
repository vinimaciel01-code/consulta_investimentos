"""
Eventos acionários da lista de empresas.

Eventos acionários são divisões, bonificações, amortizações, etc.
"""
import pandas as pd
from pandas_datareader import data as web
from investimentos.utils.data_functions import converte_datetime


def consulta_eventos(empresas, dt1, dt2):
    """Consulta aos eventos acionarios pela API do yahoo Finance.

    @empresas: lista de empresas (Tickers). Brasileiras devem ter '.SA'.
    @dt1: data inicial da consulta
    @dt2: data final da consulta
    """
    dt1 = converte_datetime(dt1)
    if dt1 == 'Erro':
        return "Erro na data de início. Formato 'DD/MM/AAAA'"

    dt2 = converte_datetime(dt2)
    if dt2 == 'Erro':
        return "Erro na data de fim. Formato 'DD/MM/AAAA'"

    lst = pd.DataFrame({})
    for empresa in empresas:
        try:
            temp = web.DataReader(
                empresa, data_source='yahoo-actions', start=dt1, end=dt2
            )
        except:
            print(f'Empresa {empresa} não listada.')
            continue

        temp.insert(0, 'empresa', empresa)
        lst = pd.concat([temp, lst], axis=0)

    lst.reset_index(inplace=True)
    return lst
