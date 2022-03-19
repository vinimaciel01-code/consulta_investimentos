"""
Divendendos distribuidos das empresas listadas.

- yahoo_dividendos: procura no site na API do Yahoo Finance.
Este site, porém, não está apresentando os dividendos atuais dos FII. Portanto,
estes serão consultados via WebScrapp diretamente no site da B3
"""
import time
import pandas as pd
from pandas_datareader import data as web

from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from investimentos.utils.data_functions import converte_datetime


def consulta_dividendos(empresas, dt1, dt2):
    """
    Procura os dividendos das empresas selecionadas, no intervalo.

    @empresas: lista de empresas (Tickers). Brasileiras devem ter '.SA'.
    @dt1: data inicial da consulta
    @dt2: data final da consulta
    @return: pd.DataFrame
    """
    dados_yahoo = yahoo_dividendos(empresas, dt1, dt2)
    dados_b3 = b3_site_fii(empresas)

    dados_dividendos = pd.concat([dados_yahoo, dados_b3])

    return dados_dividendos


def yahoo_dividendos(empresas, dt1, dt2):
    """Consulta aos dividendos pela API do yahoo Finance.

    @empresas: lista de empresas (Tickers). Brasileiras devem ter '.SA'.
    @dt1: data inicial da consulta
    @dt2: data final da consulta
    @return: pd.DataFrame
    """
    dt1 = converte_datetime(dt1)
    if dt1 == 'Erro':
        return "Erro na data de início. Formato 'DD/MM/AAAA'"

    dt2 = converte_datetime(dt2)
    if dt2 == 'Erro':
        return "Erro na data de fim. Formato 'DD/MM/AAAA'"

    lst = pd.DataFrame({})
    for empresa in empresas:
        try:
            temp = web.DataReader(
                empresa, data_source='yahoo-dividends', start=dt1, end=dt2
            )
        except:
            print(f'Empresa {empresa} não listada.')
            continue

        temp.insert(0, 'empresa', empresa)
        lst = pd.concat([temp, lst], axis=0)

    lst.index.name = 'Data'
    return lst


def b3_site_fii(empresas):
    """Abre o link de procura da B3 e procura infos dos FIIs requeridos.

    @empresas: lista das empresas FII que quero procurar
    @return: pd.DataFrame
    """
    lista_empresas = []
    for empresa in empresas:
        if '11' in empresa:
            lista_empresas.append(empresa)

    # inicializa driver
    if len(lista_empresas) == 0:
        return []

    driver = webdriver.Chrome()  # add: catch erro de drive
    driver.maximize_window()
    wdw = WebDriverWait(driver, 30000)

    # Loop pelas lista_empresas
    dados = pd.DataFrame({})
    for empresa in lista_empresas:

        # empresa e reinicia site
        empresa = empresa.replace('.SA', '')
        print(empresa)

        # url de procura do FII
        driver.get(''.join(('https://www.b3.com.br/pt_br/produtos-e-servicos/',
                            'negociacao/renda-variavel/',
                            'fundos-de-investimentos/fii/fiis-listados/')))

        # procura o FII
        locator = (By.ID, 'bvmf_iframe')
        driver.switch_to.default_content()
        elemento = wdw.until(ec.element_to_be_clickable(locator))
        driver.switch_to.frame(elemento)

        locator = (By.XPATH, '//*[@id="palavrachave"]')  # insere empresa
        elemento = wdw.until(ec.element_to_be_clickable(locator))
        for _ in range(20):
            elemento.send_keys(Keys.BACKSPACE)
        elemento.send_keys(empresa)

        locator = (By.XPATH, '//*[@id="palavrachave"]')  # insere ENTER
        driver.find_element(*locator).send_keys(Keys.ENTER)

        time.sleep(2)  # espera carregar
        locator = (By.XPATH, '//div[@class=spinner-circle-swish]')
        wdw.until_not(ec.element_to_be_clickable(locator))
        wdw.until_not(ec.presence_of_element_located(locator))

        # caixa do resultado da procura
        locator = (By.XPATH, '//*[@id="nav-bloco"]/div/div/a/div')
        elemento = wdw.until(ec.element_to_be_clickable(locator))
        driver.execute_script('arguments[0].click();', elemento)

        # Navega para a aba de eventos corporativos
        locator = (
            By.XPATH,
            ''.join(('//div[@id="divContainerIframeB3"]//',
                    'a[contains(text(), "Eventos Corporativos")]'))
        )
        elemento = wdw.until(ec.element_to_be_clickable(locator))
        driver.execute_script('arguments[0].click();', elemento)

        # Salva a tabela de PROVENTOS
        locator = (By.ID, 'bvmf_iframe')
        driver.switch_to.default_content()
        elemento = wdw.until(ec.element_to_be_clickable(locator))
        driver.switch_to.frame(elemento)

        locator = (By.ID, 'accordionBody')
        elemento = wdw.until(ec.element_to_be_clickable(locator))

        if 'show' not in elemento.get_attribute('class').split():
            print('elemento não expandido. Empresa: ', empresa)
            elemento.click()  # verifica se proventos está expandido

        table = Bs(driver.page_source, 'html.parser').find_all('table')[0]

        # transforma o html em dados
        lst = []
        columns = [i.get_text(strip=True) for i in table.find_all('th')]
        for row in table.find('tbody').find_all('tr'):
            lst.append(
                [coluna.get_text(strip=True) for coluna in row.find_all('td')]
            )

        # adiciona o nome da empresa
        lst = pd.DataFrame(lst, columns=columns)
        lst.insert(0, 'Empresa', empresa)

        # une com a lista acumulada
        dados = pd.concat([lst, dados], axis=0)

    # encerra o driver e salva
    driver.quit()
    return dados

# if __name__ == '__main__':

#     lista = ['MDIA3.SA','ITUB3.SA', 'EQIX', 'DLR']
#     data_inicial = dt.datetime(2010, 1, 1)
#     data_final = dt.datetime.today()
#     lista = yahoo_cotacao(lista, data_inicial, data_final)
