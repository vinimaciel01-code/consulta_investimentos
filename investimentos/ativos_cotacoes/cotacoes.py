"""Cotações da lista de empresas.

Cotação dosa listados no site do Yahoo Finance.
Pode ser ações, FII, stocks, Reits, títulos. etc.
"""
import pandas as pd
from pandas_datareader import data as web
import investimentos.utils.data_functions as data_functions


def consulta_cotacoes(empresas, dt1, dt2):
    """Consulta às cotações pela API do yahoo Finance.

    @empresas: lista de empresas (Tickers). Brasileiras devem ter '.SA'.
    @dt1: data inicial da consulta
    @dt2: data final da consulta
    """
    dt1 = data_functions.transforma_data(dt1)
    dt2 = data_functions.transforma_data(dt2)

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


if __name__ == '__main__':

    dt1 = '01/01/2020'
    dt2 = '31/12/2021'
    lista_ativos = ['IRBR3.SA', 'HGBS11.SA']
    dados = consulta_cotacoes(lista_ativos, dt1, dt2)
    print(dados)
