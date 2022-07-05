import os
import pandas as pd
import datetime as dt
import warnings

warnings.simplefilter('ignore')

path_download = r'C:\Users\vinim\Downloads'
path_projeto = r'C:\Users\vinim\Documents\Projetos\Investimentos'

origem_path = os.path.join(path_projeto, 'Investimentos.xlsm')
saida_caminho = os.path.join(path_projeto, 'saida')

dt1 = dt.datetime(2020, 1, 1)
dt2 = dt.datetime.today()

empresas = ['ABEV3.SA', 'ARZZ3.SA', 'HGBS11.SA', 'PLD', 'AMZN',] 
