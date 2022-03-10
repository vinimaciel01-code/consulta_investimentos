"""
Acessa as informações de FII no site da B3.

Navega para a aba de eventos corporativos
- Baixa a tabela de Proventos em dinheiro
"""

import time

import pandas as pd
from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def webscrap_b3fii(empresas):
    """Abre o link de procura da B3 e procura infos dos FIIs requeridos.

    @empresas: lista das empresas FII que quero procurar
    return: pd.DataFrame
    """
    lista_empresas = []
    for empresa in empresas:
        if '11' in empresa:
            lista_empresas.append(empresa)

    # inicializa driver
    if len(lista_empresas) == 0:
        return []

    driver = webdriver.Chrome()
    driver.maximize_window()
    wdw = WebDriverWait(driver, 30000)

    # Loop pelas lista_empresas
    dados = pd.DataFrame({})
    for empresa in lista_empresas:

        # empresa e reinicia site
        empresa = empresa.replace('.SA', '')
        print(empresa)

        # url de procura do FII
        driver.get('https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/fundos-de-investimentos/fii/fiis-listados/')

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
            '//div[@id="divContainerIframeB3"]//a[contains(text(), "Eventos Corporativos")]',
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
            lst.append([
                coluna.get_text(strip=True) for coluna in row.find_all('td')
                ])

        # adiciona o nome da empresa
        lst = pd.DataFrame(lst, columns=columns)
        lst.insert(0, 'Empresa', empresa)

        # une com a lista acumulada
        dados = pd.concat([lst, dados], axis=0)

    # encerra o driver e salva
    driver.quit()
    return dados
