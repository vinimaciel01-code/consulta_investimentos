
import pandas as pd
import time
import os
import warnings

from consulta_investimentos import consulta_eventos
import tests.config as config

lista = consulta_eventos(config.empresas, config.dt1, config.dt2)

# tratamentos
lista['Código'] = [x.replace('.SA', '') for x in lista['Código']]
lista.sort_values(['Código', 'Negociado'], ascending=True, inplace=True)
lista.reset_index(drop=True, inplace=True)
lista.fillna('', inplace=True)

# cruza com dados já existentes
if os.path.isfile(config.origem_path):
    try:
        lista_existente = pd.read_excel(
            config.origem_path, sheet_name='Py_Eventos', engine='openpyxl')
        lista_existente.fillna('', inplace=True)
        lista_existente = lista_existente.iloc[:, 0:9]
        lista = append_nao_duplicatas(lista_existente, lista, col=None)
    except Exception as erro:
        print(f'Ainda não existem dados prévios. Erro ({erro.__class__})')

# salvando
saida_path = os.path.join(config.saida_caminho, 'eventos.xlsx')
with pd.ExcelWriter(saida_path) as writer:
    lista.to_excel(writer, index=False, float_format='%.6f', sheet_name='eventos')
