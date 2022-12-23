"""Cotações da lista de empresas.

Cotação dosa listados no site do Yahoo Finance.
Pode ser ações, FII, stocks, Reits, títulos. etc.
"""
import locale
import pandas as pd
import yfinance as yf

from consulta_investimentos.utils import data_functions

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def consulta_cotacoes(empresas):

    empresas_string = ''
    for empresa in empresas:
        empresas_string = empresas_string + empresa.lower() + ' '

    tickers = yf.Tickers(empresas_string)

    close = tickers.history(period="1mo")['Close']
    dividendos = tickers.history(period="1mo")['Dividends']
    splits = tickers.history(period="1mo")['Stock Splits']

    return close, dividendos, splits