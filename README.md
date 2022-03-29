# consulta_investimentos

Consulta informações diversas de ações no Brasil e exterior

## O que faz
Esta programa faz consultas de investimentos em ações no Brasil e no Exterior pela API do Yahoo Finance. Este site apresenta limitações, como não divulgar informações de eventos acionários de Fundos de investimentos Imonibiliários (FII). Portanto, complemento a informação faltante com uma consulta no site da B3 por meio de WebScrapp.
Também existe uma função que navega pela área privada do investidor na B3, pede que o usuário faça o login, e baixa o extrato de posições atuais e movimentações históricas de ativos no Brasil ligado ao CPF do usuário.

## Funcionalidades
- Cotações: busca a cotação na moeda do ativo no site do Yahoo Finance
- Dividendos: busca os dividendos distribuidos pela API do Yahoo Finance e complementa para os FII com infos do site da B3.
- Eventos: busca os eventos acionários (distribuidos, splits, bonificações, etc.) pela API Yahoo Finance e complementa para os FII com infos do site da B3.
- Posicao: navega pelo site do investidor da B3 ('https://www.investidor.b3.com.br/'), pede que o usuário faça o login e baixa as tabelas de posição atual de ativos no Brasil e a de movimentação histórica.
- Cotacao: baixa a cotação de moedas na API do Exchange Rate ('https://api.exchangerate.host/timeseries')

## Preparação
1. Instalar configuração de browser do Selenium, para permitir que abra um browser automatizado. https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
2. Instalar este pacote e suas dependências (no arquivo pyproject.toml) 
`poetry install bbscrap`

## Como usar

Existe uma função para cada funcionalidade descrita

`import investimentos`

`dados_cotacoes = investimentos.consulta_cotacoes(empresas, dt1, dt2)`
`dados_dividendos = consulta_dividendos(empresas, dt1, dt2)`
`dados_eventos = consulta_eventos(empresas, dt1, dt2)`
`dados_posicao = consulta_posicao(path_download, dt1, dt2)`
`dados_moedas = consulta_moedas(valor, moeda_base, moeda_destino, dt1=None, dt2=None)`

Sendo que:
- Empresas: lista de empresas a fazer a consulta
- dt1: data inicial da consulta
- dt2: data final da consulta
- path_download: path_download: caminho completo da pasta de downloads (Ex.: C:/user/fulano/downloads)
- moeda_base: código da moeda que quero converter (Ex: 'BRL')
- moeda_destino: moeda para a qual quero converter (Ex.: 'USD')
- valor: quantidade de moedas base que quero converter)
