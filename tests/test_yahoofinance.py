
from investimentos import ativos


dt1 = '01/01/2020'
dt2 = '01/02/2022'
lista_ativos = ['IRBR3.SA', 'HGBS11.SA']

"Testando ativos"
dados = ativos.yahoo_cotacao(lista_ativos, dt1, dt2)
dados = ativos.yahoo_eventos(lista_ativos, dt1, dt2)
dados = ativos.yahoo_dividendos(lista_ativos, dt1, dt2)
print(dados)
