import app.api_yahoofinance as yahoo

empresas = ['HGBS11'] #,'NEXISTE']
dt1 = '01/01/2021'
dt2 = '31/12/2021'

dados = yahoo.yahoo_cotacao(empresas, dt1, dt2)
dados = yahoo.yahoo_dividendos(empresas, dt1, dt2)
dados = yahoo.yahoo_eventos(empresas, dt1, dt2)
