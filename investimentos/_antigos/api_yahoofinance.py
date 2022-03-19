"""
Busca as informações da lista de empresas, entre duas datas.

- yahoo yahoo_cotacao
- yahoo yahoo_eventos
- yahoo yahoo_dividendos
"""
import warnings

import pandas as pd
from pandas_datareader import data as web

from investimentos.utils.data_functions import converte_datetime

warnings.simplefilter('ignore')  # para ignorar o aviso do read_excel


def yahoo_cotacao(empresas, dt1, dt2):
    """Consulta às cotações pela API do yahoo Finance.

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

    lst = pd.DataFrame({'Date': []})
    for empresa in empresas:
        try:
            temp = web.DataReader(
                empresa, data_source='yahoo', start=dt1, end=dt2
            )
        except:
            print(f'Empresa {empresa} não listada.')
            continue

        temp.rename(columns={'Adj Close': empresa}, inplace=True)
        temp = round(temp[empresa], 2)
        lst = pd.merge(temp, lst, on='Date', how='outer')

    lst.set_index('Date', inplace=True)
    lst.sort_index(axis=0, inplace=True, ascending=False)
    lst.index.name = 'Data'
    return lst


def yahoo_eventos(empresas, dt1, dt2):
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


def yahoo_dividendos(empresas, dt1, dt2):
    """Consulta aos dividendos pela API do yahoo Finance.

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
                empresa, data_source='yahoo-dividends', start=dt1, end=dt2
            )
        except:
            print(f'Empresa {empresa} não listada.')
            continue

        temp.insert(0, 'empresa', empresa)
        lst = pd.concat([temp, lst], axis=0)

    lst.index.name = 'Data'
    return lst


# if __name__ == '__main__':

#     lista = ['MDIA3.SA','ITUB3.SA', 'EQIX', 'DLR']
#     data_inicial = dt.datetime(2010, 1, 1)
#     data_final = dt.datetime.today()
#     lista = yahoo_cotacao(lista, data_inicial, data_final)
