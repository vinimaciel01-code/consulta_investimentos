"""
API: yahoo finance
Busca as informações da lista de empresas, entre duas datas
"""

import warnings

import pandas as pd
from pandas_datareader import data as web

import app.utils.data_functions as datavalida

warnings.simplefilter('ignore')  # para ignorar o aviso do read_excel


def yahoo_cotacao(empresas, dt1, dt2):
    """
    Consulta às cotações pela API do yahoo Finance
    """

    if datavalida.valida(dt1) is False or datavalida.valida(dt2) is False:
        return 'Yahoo Finance cotação: Erro na data.'

    lst = pd.DataFrame({'Date': []})
    for empresa in empresas:
        temp = web.DataReader(
            empresa, data_source='yahoo', start=dt1, end=dt2
        )
        temp.rename(columns={'Adj Close': empresa}, inplace=True)
        temp = round(temp[empresa], 2)
        lst = pd.merge(temp, lst, on='Date', how='outer')

    lst.set_index('Date', inplace=True)
    lst.sort_index(axis=0, inplace=True, ascending=False)
    lst.index.name = 'Data'
    return lst


def yahoo_eventos(empresas, dt1, dt2):
    """
    Consulta aos eventos acionarios pela API do yahoo Finance
    """

    if datavalida.valida(dt1) is False or datavalida.valida(dt2) is False:
        return 'Yahoo Finance eventos: Erro na data.'

    lst = pd.DataFrame({})
    for empresa in empresas:
        temp = web.DataReader(
            empresa,
            data_source='yahoo-actions',
            start=dt1,
            end=dt2,
        )
        temp.insert(0, 'empresa', empresa)
        lst = pd.concat([temp, lst], axis=0)

    lst.reset_index(inplace=True)
    return lst


def yahoo_dividendos(empresas, dt1, dt2):
    """
    Consulta aos dividendos pela API do yahoo Finance
    """

    if datavalida.valida(dt1) is False or datavalida.valida(dt2) is False:
        return 'Yahoo Finance eventos: Erro na data.'

    lst = pd.DataFrame({})
    for empresa in empresas:
        temp = web.DataReader(
            empresa,
            data_source='yahoo-dividends',
            start=dt1,
            end=dt2,
        )
        temp.insert(0, 'empresa', empresa)
        lst = pd.concat([temp, lst], axis=0)

    lst.index.name = 'Data'
    return lst


# if __name__ == '__main__':

#     lista = ['MDIA3.SA','ITUB3.SA', 'EQIX', 'DLR']
#     data_inicial = dt.datetime(2010, 1, 1)
#     data_final = dt.datetime.today()
#     lista = yahoo_cotacao(lista, data_inicial, data_final)
