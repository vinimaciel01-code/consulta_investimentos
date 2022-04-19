"""
Acessa a área de investidor do site da B3 (https://www.investidor.b3.com.br/).

Faz o login manualmente e baixa as informações de todos os ativos
"""
import datetime as dt
import os
import warnings

import pandas as pd
from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from consulta_investimentos.utils.arquivo import download_concluido
from consulta_investimentos.utils import data_functions


def consulta_posicao(path_download, dt1, dt2):
    """
    Faz o login na área privada de investidor no site da B3.

    @param path_download: caminho da pasta de Downloads
    @param dt1: data inicial da procura dos dados
    @param dt2: data final da procura dos dados
    Return: dados da posição, dados das movimentações
    """
    dt1 = data_functions.transforma_data(dt1)
    dt2 = data_functions.transforma_data(dt2)
    if dt1 > dt2:
        print('Data de início maior que data de fim')
        return pd.DataFrame()

    if dt1 < dt.datetime(2019, 11, 1):
        dt1 = dt.datetime(2019, 11, 1)
    if dt2.date() >= dt.datetime.today().date():
        dt2 = dt.datetime.today() + dt.timedelta(days=-1)

    # Inicializa
    driver = webdriver.Chrome()
    driver.maximize_window()
    wdw = WebDriverWait(driver, 15)
    driver.get('https://www.investidor.b3.com.br/')

    # espera aparecer o elemento da senha
    locator = (By.ID, 'DOC_INPUT')
    wdw.until(ec.element_to_be_clickable(locator))
    print('Página carregada com sucesso')
    print('Faça o Login e responda à pergunta de segurança.')

    # pausa para a senha
    # espera o elemento surgir para continuar

    # Ele abre em uma tela diferente, mas depois
    # que clica em qualque opcao, continua na tela
    # padrao anterior

    locator = (
        By.XPATH,
        "//button[contains(text(), 'Ir para Extrato de Posição')]",
    )
    while True:
        try:
            driver.find_element(*locator)
            print('Login realizado')
            break
        except:
            pass

    # botao aceitar cookies
    try: 
        locator = (By.ID, 'onetrust-accept-btn-handler')
        wdw.until(ec.element_to_be_clickable(locator)).click()
    except: 
        pass

    # Navega para a pagina central (que contém as abas)
    # Utiliza a aba de posição
    locator = (By.XPATH,"//button[contains(text(), 'Ir para Extrato de Posição')]")
    element = driver.find_element(*locator)
        
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    driver.find_element(*locator).click()

    # dados de posição
    dados_pos = scrap_posicao(driver)

    # dados de movimentação
    dados_mov = scrap_movimentacao(driver, path_download, dt1, dt2)

    # Finaliza
    driver.quit()
    return dados_pos, dados_mov


def scrap_posicao(driver):
    """Baixa a posição atual de todos os ativos.

    @param driver: driver selenium da página
    @param path_download: caminho da pasta de Downloads
    @param dt1: data inicial da procura dos dados
    @param dt2: data final da procura dos dados
    """
    wdw = WebDriverWait(driver, 15)
    dados = pd.DataFrame({})

    # navegacao para a aba de movimentação
    locator = (By.ID, 'Posição')
    wdw.until(ec.element_to_be_clickable(locator)).click()

    # baixa todas as tabelas
    locator = (By.XPATH, "//div[@class='b3i-tabela-conteudo__tabela']")
    wdw.until(ec.element_to_be_clickable(locator))
    tables = Bs(driver.page_source, 'html.parser').find_all('table')

    # Tabela de ações
    table = tables[0]
    dados_acao = []
    columns = [i.get_text(strip=True) for i in table.find_all('th')]
    for row in table.find('tbody').find_all('tr'):
        dados_acao.append(
            [coluna.get_text(strip=True) for coluna in row.find_all('td')]
        )
    dados_acao = pd.DataFrame(dados_acao, columns=columns)

    # Formata variaveis
    dados_acao['Valor atualizado'] = [
        x.replace('Ver mais', '') for x in dados_acao['Valor atualizado']
    ]
    dados_acao = dados_acao.drop('', axis=1)

    # Tabela de FII
    table = tables[1]
    dados_fii = []
    columns = [i.get_text(strip=True) for i in table.find_all('th')]
    for row in table.find('tbody').find_all('tr'):
        dados_fii.append(
            [coluna.get_text(strip=True) for coluna in row.find_all('td')]
        )
    dados_fii = pd.DataFrame(dados_fii, columns=columns)

    # Formata variaveis
    dados_fii['Valor atualizado'] = [
        x.replace('Ver mais', '') for x in dados_fii['Valor atualizado']
    ]
    dados_fii = dados_fii.drop('', axis=1)

    # une com a lista acumulada
    dados = pd.concat([dados_acao, dados_fii], axis=0)

    return dados


def scrap_movimentacao(driver, path_download, dt1, dt2):
    """
    Baixa o histórico de movimentações de ações.

    @param driver: driver selenium da página
    @param path_download: caminho da pasta de Downloads
    @param dt1: data inicial da procura dos dados
    @param dt2: data final da procura dos dados
    """
    dt1 = data_functions.transforma_data(dt1)
    dt2 = data_functions.transforma_data(dt2)
    if dt1 > dt2:
        print('Data de início maior que data de fim')
        return pd.DataFrame()

    wdw = WebDriverWait(driver, 15)

    # navegacao para a aba de movimentação
    locator = (By.ID, 'Movimentação')
    wdw.until(ec.element_to_be_clickable(locator)).click()

    dados_mov = pd.DataFrame({})
    
    # ajusta na data dt2, que tem que ser menor que o dia de hoje
    if dt2.date() == dt.datetime.today().date():
        dt2 = dt2 - dt.timedelta(days=1)

    dt_min = dt1 - dt.timedelta(days=1)
    dt_max = dt_min
    
    while True:

        # Saida
        if (dt_max - dt2).days == 0:
            break

        # Atualiza datas
        dt_min = dt_max + dt.timedelta(days=1)

        if (dt2 - dt_min).days > 365:            
            dt_max = dt_min + dt.timedelta(days=365)
        else:
            dt_max = dt2

        # navegação no pop-up de filtros
        locator = (By.XPATH, '//div[@class="b3-filtrar"]/button')
        wdw.until(ec.element_to_be_clickable(locator)).click()

        locator = (By.XPATH, "//input[@data-placeholder='Data final']")
        elemento = wdw.until(ec.element_to_be_clickable(locator))
        for _ in range(10):
            elemento.send_keys(Keys.BACKSPACE)
        elemento.send_keys(dt_max.strftime('%d/%m/%Y'))

        locator = (By.XPATH, "//input[@data-placeholder='Data inicial']")
        elemento = wdw.until(ec.element_to_be_clickable(locator))
        for _ in range(10):
            elemento.send_keys(Keys.BACKSPACE)
        elemento.send_keys(dt_min.strftime('%d/%m/%Y'))

        # volta à data final -> aplica a conferencia do campo na data inicial
        locator = (By.XPATH, "//input[@data-placeholder='Data final']")
        elemento = wdw.until(ec.element_to_be_clickable(locator)).click()

        # Futuro !
        # procurar se houve erro de data

        locator = (By.ID, 'botao-filtrar-movimentacao')
        wdw.until(ec.element_to_be_clickable(locator)).click()

        locator = (By.ID, 'botao-download-movimentacao')
        wdw.until(ec.element_to_be_clickable(locator)).click()

        locator = (By.XPATH, '//*[@id="botao-movimentacao-excel"]')
        wdw.until(ec.element_to_be_clickable(locator)).click()

        locator = (By.XPATH, '//div[@class="fechar"]/button')
        wdw.until(ec.element_to_be_clickable(locator)).click()

        # ler arquivo recem baixado
        download_concluido(path_download)
        pasta_baixados = os.listdir(path_download)
        pasta_baixados = [d for d in pasta_baixados if '.xls' in d]
        pasta_baixados = [
            os.path.join(path_download, d) for d in pasta_baixados
        ]
        pasta_novato = max(pasta_baixados, key=os.path.getctime)

        with warnings.catch_warnings(record=True):
            warnings.simplefilter('always')
            arquivo_novo = pd.read_excel(pasta_novato, engine='openpyxl')

        arquivo_novo['Produto'] = arquivo_novo['Produto'].str.strip()
        arquivo_novo['Código'] = arquivo_novo['Produto'].str.split(
            ' - ', 1, expand=True
        )[0]
        dados_mov = pd.concat([arquivo_novo, dados_mov], axis=0)

        # atualiza a data inicial (loop)
        dt_min = dt_max + dt.timedelta(days=1)

    return dados_mov


if __name__ == '__main__':

    dt1 = dt.datetime(2019, 11, 1)
    dt2 = dt.datetime.today()
    path_download = r'C:\Users\vinim\Downloads'
    consulta_posicao(path_download, dt1, dt2)
