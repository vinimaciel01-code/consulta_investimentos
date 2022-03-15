import cotacoes_moeda
import ativos

dt1 = '01/01/2020'
dt2 = '01/02/2022'
lista_ativos = ['IRBR3.SA', 'HGBS11.SA']

"Testando cotacoes_moeda"
# cotacoes_moeda.imprime_teste()
# print(cotacoes_moeda.valida_moeda('USD'))
# dados = cotacoes_moeda.get_rates(1, 'USD', 'BRL')
# print(dados)

"Testando yahoo"
# dados = ativos.yahoo_cotacao(lista_ativos, dt1, dt2)
# dados = ativos.yahoo_eventos(lista_ativos, dt1, dt2)
# dados = ativos.yahoo_dividendos(lista_ativos, dt1, dt2)
# print(dados)

"Testando webscrap"
# dados = ativos.scrap_fii(lista_ativos)
dados = ativos.scrap_investidor(r'C:\Users\vinim\Downloads', dt1, dt2)
print(dados)
