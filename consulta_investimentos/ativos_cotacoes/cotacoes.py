"""Cotações da lista de empresas.

Cotação dosa listados no site do Yahoo Finance.
Pode ser ações, FII, stocks, Reits, títulos. etc.
"""
import pandas as pd
from pandas_datareader import data as web

from consulta_investimentos.utils import data_functions


def consulta_cotacoes(empresas, dt1, dt2):
    """Consulta às cotações pela API do yahoo Finance.

    @empresas: lista de empresas (Tickers). Brasileiras devem ter '.SA'.
    @dt1: data inicial da consulta (dd/mm/aaaa)
    @dt2: data final da consulta (dd/mm/aaaa)
    """
    dt1 = data_functions.transforma_data(dt1)
    dt2 = data_functions.transforma_data(dt2)
    if dt1 is None:
        print('Data de início Vazia')
        return pd.DataFrame()
    if dt2 is None:
        dt2 = dt1
    if dt1 > dt2:
        print('Data de início maior que data de fim')
        return pd.DataFrame()

    lst = pd.DataFrame({'Date': []})
    for empresa in empresas:
        print(empresa)

        for _ in range(1, 4):
            try:
                erro = False
                temp = pd.DataFrame({})
                temp = web.DataReader(
                    empresa, data_source='yahoo',
                    start=dt1, end=dt2)
                break
            except:
                erro = True
                continue

        if erro is True:
            print('Empresa não encontrada.')
            continue

        temp.rename(columns={'Adj Close': empresa}, inplace=True)
        temp = round(temp[empresa], 2)
        lst = pd.merge(temp, lst, on='Date', how='outer')

    lst.set_index('Date', inplace=True)
    lst.sort_index(axis=0, inplace=True, ascending=False)
    lst.index.name = 'Data'
    return lst

if __name__ == '__main__':

    empresas = ['IRBR3.SA', 'HGBS11.SA', 'V', 'STOR']
    dt1 = ''
    dt2 = '31/12/2021'
