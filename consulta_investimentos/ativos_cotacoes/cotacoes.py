"""Cotações da lista de empresas.

Cotação dosa listados no site do Yahoo Finance.
Pode ser ações, FII, stocks, Reits, títulos. etc.
"""
import locale
import yfinance as yf

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def consulta_cotacoes(empresas, data_inicio=None, periodo=None):

    empresas_string = ''
    for empresa in empresas:
        empresas_string = empresas_string + empresa.lower() + ' '

    tickers = yf.Tickers(empresas_string)

    if data_inicio is not None:

        close = tickers.history(start=data_inicio)['Close']
        dividendos = tickers.history(start=data_inicio)['Dividends']
        splits = tickers.history(start=data_inicio)['Stock Splits']

    else:

        close = tickers.history(start="2000-01-01")['Close']
        dividendos = tickers.history(start="2000-01-01")['Dividends']
        splits = tickers.history(start="2000-01-01")['Stock Splits']

    return close, dividendos, splits