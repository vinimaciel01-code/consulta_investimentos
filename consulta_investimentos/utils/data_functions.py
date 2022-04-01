"""Funções de manipulação e testes em Datas."""

import datetime as dt


def valida(data):
    """Valida se a data é válida (Date ou Datetime).

    @param data: string ou datetime
    @return: boolean
    """
    if isinstance(data, dt.datetime):
        return True

    if isinstance(data, dt.date):
        return True

    return False


def converte_datetime(data):
    """Retorna a data convertida para 'datetime.datetime'.

    @param data: string ou datetime formatada
    @return: dt.datetime
    """
    if valida(data):
        if isinstance(data, dt.datetime):
            return data
        if isinstance(data, dt.date):
            return dt.datetime.combine(data, dt.datetime.min.time())

    if data is None or data == '':
        return

    if isinstance(data, str):
        try:
            return dt.datetime.strptime(data, '%d/%m/%Y')
        except Exception as erro:
            raise ValueError(
                f'Data "{data}" com formato inválido. invalida. Erro ({erro.__class__})'
            ) from erro
    else:
        raise ValueError('Erro: nao se encaixou nos casos especificados.')


def transforma_data(data):
    """Transforma uma data e a limita entre jan00 e hoje.

    A data deve existir e ser maior ou igual a 01/01/2000.
    @param data: datetime
    @return: data
    """
    data = converte_datetime(data)

    if data is None:
        return None

    if data > dt.datetime.today():
        return dt.datetime.today()

    if data < dt.datetime(2000, 1, 1):
        return dt.datetime(2000, 1, 1)

    return data


if __name__ == '__main__':

    data = ''

    print(valida(data))
    print(converte_datetime(data))
    print(transforma_data(data))
