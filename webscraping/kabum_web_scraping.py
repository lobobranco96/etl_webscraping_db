from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import pandas as pd
import time
import math
import re
import datetime

hardware = ['ssd-2-5', 'coolers', 'fontes', 'placa-de-video-vga', 'disco-rigido-hd', 'memoria-ram', 'placas-mae', 'processadores']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}


def ws(item):
    url = f'https://www.kabum.com.br/hardware/{item}'    # caminho do site, podendo mudar conforme sua escolha
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    driver.get(url)

    time.sleep(2)
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    qtd_itens = soup.find('div', id='listingCount').get_text().strip()

    index = qtd_itens.find(' ')
    qtd = qtd_itens[:index]
    ultima_pagina = math.ceil(int(qtd) / 20)

    # Estrutura de dados para armazenar os resultados
    produtos = {'Descrição': [], 'Preço em R$': []}

    for i in range(1, ultima_pagina + 1):
        url_pag = f'{url}?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
        driver.get(url_pag)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        produtos_pagina = soup.find_all('div', class_=re.compile('productCard'))

        for produto in produtos_pagina:
            marca = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
            preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip()
            preco = preco[2:].replace('\xa0', '').replace('----', '0')

            produtos['Descrição'].append(marca)
            produtos['Preço em R$'].append(preco)

    driver.quit()

    catalago_kabum = pd.DataFrame(produtos)
    catalago_kabum.index.name = 'ID'

    catalago_kabum.to_csv(
        f'C:/Users/Renato/Desktop/Engenharia de dados/ETL/webscraping/excel_file/{item}_{data_atual}.csv',
        encoding='utf-8', sep=';')


for tipo_produto in hardware:
    ws(tipo_produto)