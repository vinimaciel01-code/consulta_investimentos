"""
Busca as cotações na API da exchangerate
API: https://exchangerate.host
"""
import datetime as dt
import requests
import pandas as pd

from app.utils.data_functions import converte_datetime


def valida_moeda(moeda):
    """Valida a moeda e converte para uppercase"""

    url = 'https://api.exchangerate.host/symbols'
    response = requests.get(url)
    data = response.json()

    lista_simbols = []
    for item in data['symbols']:
        lista_simbols.append(item)

    moeda = moeda.upper()
    if moeda not in lista_simbols:
        return (
            'Erro: moeda não está na lista de códigos permitidos ('
            + ''.join(str(x + ',') for x in lista_simbols)
            + ')'
        )
    else:
        return moeda


def get_rates(valor, moeda_base, moeda_destino, data_inicio, data_fim):

    """
    Retorna a cotação de uma moeda, entre duas datas.
    Valor: valor da moeda_base que irei converter
    Moeda_base: moeda que quero converter
    Moeda_destino: moeda para a qual quero converter
    Data_inicio: formato 'DD/MM/AAAA'
    Data_fim: formato 'DD/MM/AAAA'
    """

    # valida: datas informadas
    dt1 = converte_datetime(data_inicio)
    if dt1 == 'Erro':
        return "Erro na data de início. Formato 'DD/MM/AAAA'"

    dt2 = converte_datetime(data_fim)
    if dt2 == 'Erro':
        return "Erro na data de fim. Formato 'DD/MM/AAAA'"

    if dt1 < dt.datetime(2000, 1, 1):
        dt1 = dt.datetime(2000, 1, 1)
    if dt2 > dt.datetime.today():
        dt2 = dt.datetime.today()

    # valida: moeda informadas
    moeda_base = valida_moeda(moeda_base)
    if 'Erro' in moeda_base:
        return moeda_base

    moeda_destino = valida_moeda(moeda_destino)
    if 'Erro' in moeda_destino:
        return moeda_destino

    # inicializa variaveis
    moeda_historico = pd.DataFrame({})
    dt_max = ''

    while True:

        # set datas: a API retorna apenas a cotação para 365 dias

        if dt_max == dt2:
            break
        if dt_max != '':
            dt1 = dt_max + dt.timedelta(days=1)

        dt_dif = (dt2 - dt1).days
        if dt_dif > 365:
            dt_max = dt1 + dt.timedelta(days=365)
        else:
            dt_max = dt2

        # requests
        # Permite que forneça os argumentos (params) como um dicionário
        url = r'https://api.exchangerate.host/timeseries'
        payload = {
            'base': moeda_base,
            'amount': valor,
            'start_date': dt1,
            'end_date': dt_max,
        }
        response = requests.get(url, params=payload)
        data = response.json()

        # armazenar os data
        moeda_dados = {}  # dict

        for item in data['rates']:
            moeda_data = item
            moeda_rate = data['rates'][item][moeda_destino]
            moeda_dados[moeda_data] = moeda_rate

        # clean data
        pd_data = pd.DataFrame.from_records(
            data=moeda_dados, index=[0]
        ).transpose()
        pd_data.columns = [str(valor) + moeda_base + ':' + moeda_destino]

        # reunir com os outros data
        moeda_historico = pd.concat([moeda_historico, pd_data], axis=0)
        moeda_historico.sort_index(
            axis=0, ascending=True, inplace=True
        )  # ascending para o PROCV verdadeiro funcionar no excel

    moeda_historico.reset_index(inplace=True)
    moeda_historico = moeda_historico.rename(
        columns={'index': 'Data'}, inplace=False
    )
    moeda_historico['Data'] = pd.to_datetime(moeda_historico['Data'])

    return moeda_historico
