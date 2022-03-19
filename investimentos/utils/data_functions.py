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


def valida_duas_datas(dt1, dt2):
    """Recebe duas datas. Retorna as datas corrigidas ou erro.

    @param dt1: data inicial
    @param dt2: data final
    @return: dt1, dt2 OU erro
    """
    if dt1 is None:
        dt1 = dt.datetime.today()
    dt1 = converte_datetime(dt1)

    if dt2 is None or dt2 < dt1:
        dt2 = dt1
    dt2 = converte_datetime(dt2)

    if dt1 < dt.datetime(2000, 1, 1):
        dt1 = dt.datetime(2000, 1, 1)
    if dt2 > dt.datetime.today():
        dt2 = dt.datetime.today()

    return dt1, dt2


def converte_datetime(data):
    """Retorna a data convertida para 'datetime.datetime'.

    @param data: string ou datetime formatada
    @return: dt.datetime
    """
    if isinstance(data, dt.datetime):
        return data

    if isinstance(data, dt.date):
        return dt.datetime.combine(data, dt.datetime.min.time())

    if isinstance(data, str):
        try:
            return dt.datetime.strptime(data, '%d/%m/%Y')
        except Exception as erro:
            raise ValueError(
                f'Data "{data}" invalida. Erro ({erro.__class__})'
            ) from erro
    else:
        raise ValueError('Erro: nao se encaixou nos casos especificados.')


if __name__ == '__main__':

    dt1 = dt.datetime(2020, 1, 1)
    dt2 = dt.datetime(2022, 1, 1)

    print(valida(dt1))
    print(isinstance(converte_datetime(dt1), dt.datetime))
    print(valida_duas_datas(dt1, dt2))
