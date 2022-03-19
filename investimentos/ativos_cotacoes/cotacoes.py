"""Cotações da lista de empresas.

Cotação dosa listados no site do Yahoo Finance.
Pode ser ações, FII, stocks, Reits, títulos. etc.
"""
import pandas as pd
from pandas_datareader import data as web
from investimentos.utils.data_functions import converte_datetime


def consulta_cotacoes(empresas, dt1, dt2):
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
