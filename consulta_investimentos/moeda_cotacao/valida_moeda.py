"""
Valida a moeda.

API: https://exchangerate.host
"""
import requests


def valida_moeda(moeda):
    """Valida a moeda e converte para uppercase.

    @params moeda: moeda a converter
    """
    url = 'https://api.exchangerate.host/symbols'
    response = requests.get(url)
    data = response.json()

    lista_simbols = []
    for item in data['symbols']:
        lista_simbols.append(item)

    moeda = moeda.upper()
    if moeda not in lista_simbols:
        raise ValueError(
            'Erro: moeda não está na lista de códigos permitidos ('
            + ''.join(str(x + ',') for x in lista_simbols)
            + ')'
        )

    return moeda
