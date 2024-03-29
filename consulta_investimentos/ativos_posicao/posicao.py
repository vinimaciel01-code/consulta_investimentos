"""
Acessa a área de investidor do site da B3 (https://www.investidor.b3.com.br/).

Faz o login manualmente e baixa as informações de todos os ativos
"""

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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


def consulta_posicao(path_download, dt1, dt2, login, senha):
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

    # espera aparecer o elemento do login (CPF)

    locator = (By.ID, 'cpf_mask')
    elemento = wdw.until(ec.element_to_be_clickable(locator))

    if login:
        elemento.send_keys(login)
        locator = (By.XPATH,"/html/body/app-root/app-landing-page/div/div[2]/aside/div[1]/button")
        wdw.until(ec.element_to_be_clickable(locator)).click()

    if senha:    
        locator = (By.ID, 'PASS_INPUT')
        elemento = wdw.until(ec.element_to_be_clickable(locator))
        elemento.send_keys(senha)
    
    print('Faça o Login e responda à pergunta de segurança.')

    ### pausa para responder à pergunta de segurança ###
        
    locator = (
        By.XPATH,
        "//button[contains(text(), 'Ir para posição')]",
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
    locator = (By.XPATH,"//button[contains(text(), 'Ir para posição')]")
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

    # navegacao para a aba de posição
    locator = (By.ID, 'Posição')
    wdw.until(ec.element_to_be_clickable(locator)).click()

    # baixa todas as tabelas
    locator = (By.XPATH, "//th[contains(text(), 'Produto')]")
    wdw.until(ec.element_to_be_clickable(locator))
    tables = Bs(driver.page_source, 'html.parser').find_all('table')

    # Le os dados de todas tabelas e une em um só DataFrame
    dados_posicao = pd.DataFrame({})
    for table in tables: 
        dados_table = []
        columns = [i.get_text(strip=True) for i in table.find_all('th')]
        for row in table.find('tbody').find_all('tr'):
            dados_table.append([coluna.get_text(strip=True) for coluna in row.find_all('td')])
        
        dados_table = pd.DataFrame(dados_table, columns=columns)
        dados_posicao = pd.concat([dados_posicao, dados_table])

    return dados_posicao


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

    # ajusta na data dt2, que tem que ser menor que o dia de hoje
    if dt2.date() == dt.datetime.today().date():
        dt2 = dt2 - dt.timedelta(days=1)

    dt_min = dt1 - dt.timedelta(days=1)
    dt_max = dt_min
    
    arquivos_baixados_list = []
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
        locator = (By.XPATH, '//*[@id="b3i-conteudo"]/app-extrato/div/div/div[3]/app-movimentacoes/app-tabela-filtro/div/div/button[1]')
        wdw.until(ec.element_to_be_clickable(locator)).click()

        locator = (By.XPATH, '//*[@class="form-control input-end b3-ga-datepicker"]')
        elemento = wdw.until(ec.element_to_be_clickable(locator))
        for _ in range(10):
            elemento.send_keys(Keys.BACKSPACE)
        elemento.send_keys(dt_max.strftime('%d/%m/%Y'))

        locator = (By.XPATH, '//*[@class="form-control input-start b3-ga-datepicker"]')
        elemento = wdw.until(ec.element_to_be_clickable(locator))
        for _ in range(10):
            elemento.send_keys(Keys.BACKSPACE)
        elemento.send_keys(dt_min.strftime('%d/%m/%Y'))

        locator = (By.XPATH, '//*[@class="form-control input-end b3-ga-datepicker"]') # volta à data final -> aplica a conferencia do campo na data inicial
        elemento = wdw.until(ec.element_to_be_clickable(locator)).click()

        locator = (By.ID, 'botao-filtrar-movimentacao')
        wdw.until(ec.element_to_be_clickable(locator)).click()

        # Futuro !
        # procurar se houve erro de data

        locator = (By.XPATH, '//button[@label="Baixar extrato"]')
        wdw.until(ec.element_to_be_clickable(locator)).click()

        locator = (By.XPATH, '//*[@id="b3i-conteudo"]/app-extrato/div/div/div[3]/app-movimentacoes/app-modal-download-extrato/b3-modal-drawer/div[1]/div[2]/div/div/div/app-opcoes-selecao-download/label[2]/div')
        wdw.until(ec.element_to_be_clickable(locator)).click()

        locator = (By.XPATH, '//*[@id="b3i-conteudo"]/app-extrato/div/div/div[3]/app-movimentacoes/app-modal-download-extrato/b3-modal-drawer/div[1]/div[2]/div/div/button')
        wdw.until(ec.element_to_be_clickable(locator)).click()

        import time
        time.sleep(2)
        download_concluido(path_download)

        locator = (By.XPATH, '//*[@id="b3i-conteudo"]/app-extrato/div/div/div[3]/app-movimentacoes/app-modal-download/b3-modal-drawer/div[1]/div[2]/div/div/div/button')
        wdw.until(ec.element_to_be_clickable(locator)).click()

        # ler arquivo recem baixado
        pasta_baixados = os.listdir(path_download)
        pasta_baixados = [d for d in pasta_baixados if '.xls' in d]
        pasta_baixados = [os.path.join(path_download, d) for d in pasta_baixados]
        pasta_novato = max(pasta_baixados, key=os.path.getctime)
        
        arquivos_baixados_list.append(pasta_novato)

        # atualiza a data inicial (loop)
        dt_min = dt_max + dt.timedelta(days=1)

    dados_mov = pd.DataFrame()
    for arquivo in arquivos_baixados_list:
        
        with warnings.catch_warnings(record=True):
            warnings.simplefilter('always')
            arquivo_novo = pd.read_excel(arquivo, engine='openpyxl')
            print(arquivo_novo)

        arquivo_novo['Produto'] = arquivo_novo['Produto'].str.strip()
        arquivo_novo['Código'] = arquivo_novo['Produto'].str.split(' - ', 1, expand=True)[0]
        dados_mov = pd.concat([arquivo_novo, dados_mov], axis=0)

    return dados_mov
