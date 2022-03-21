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
        print(empresa)
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
    lista_ativos = [
        'ABEV3.SA',
        'ARZZ3.SA',
        'EGIE3.SA',
        'EZTC3.SA',
        'FLRY3.SA',
        'HYPE3.SA',
        'IRBR3.SA',
        'ITUB3.SA',
        'LREN3.SA',
        'MDIA3.SA',
        'MULT3.SA',
        'PSSA3.SA',
        'RADL3.SA',
        'WEGE3.SA',
        'XPBR31.SA',
        'YDUQ3.SA',
        'GGRC11.SA',
        'HGBS11.SA',
        'HGLG11.SA',
        'HGRE11.SA',
        'HGRU11.SA',
        'KNRI11.SA',
        'RBVA11.SA',
        'VISC11.SA',
        'XPLG11.SA',
        'XPML11.SA',
        'AMT',
        'AVB',
        'DLR',
        'EQIX',
        'ESS',
        'EXR',
        'O',
        'ONL',
        'PLD',
        'PSA',
        'STOR',
        'TRNO',
        'AAPL',
        'ADBE',
        'AMZN',
        'ASML',
        'COST',
        'DIS',
        'FAST',
        'GOOGL',
        'JNJ',
        'JPM',
        'MA',
        'MSFT',
        'NVDA',
        'V',
    ]
    dados = consulta_cotacoes(lista_ativos, dt1, dt2)
    print(dados)
