import app.api_exchangerate as exchange

dados = exchange.get_rates(1, 'USD', 'BRL', '01/01/2020', '01/01/2021')