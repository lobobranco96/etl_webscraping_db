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
    """
    Esta função realiza o scraping dos dados dos produtos de hardware de uma página específica do site Kabum e os armazena em arquivos CSV.

    Parâmetros:
    - item (str): A categoria de hardware a ser pesquisada.

    Retorna:
    - None
    """
    # URL base para a categoria de hardware
    url = f'https://www.kabum.com.br/hardware/{item}'    # caminho do site, podendo mudar conforme sua escolha

    # Configurações do webdriver para navegação headless
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Acessa a página da categoria de hardware
    driver.get(url)

    # Aguarda 2 segundos para a página carregar completamente
    time.sleep(2)

    # Obtém a data atual no formato YYYY-MM-DD
    data_atual = datetime.datetime.now().strftime("%Y-%m-%d")

   # Parseia a página HTML com BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extrai a quantidade total de itens na categoria
    qtd_itens = soup.find('div', id='listingCount').get_text().strip()
    index = qtd_itens.find(' ')
    qtd = qtd_itens[:index]
    ultima_pagina = math.ceil(int(qtd) / 20)

    # Estrutura de dados para armazenar os resultados
    produtos = {'Descrição': [], 'Preço em R$': []}

    # Itera sobre todas as páginas da categoria
    for i in range(1, ultima_pagina + 1):
        url_pag = f'{url}?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
        driver.get(url_pag)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        produtos_pagina = soup.find_all('div', class_=re.compile('productCard'))

        # Extrai os dados dos produtos da página atual  
        for produto in produtos_pagina:
            marca = produto.find('span', class_=re.compile('nameCard')).get_text().strip()
            preco = produto.find('span', class_=re.compile('priceCard')).get_text().strip()
            preco = preco[2:].replace('\xa0', '').replace('----', '0')

            produtos['Descrição'].append(marca)
            produtos['Preço em R$'].append(preco)

    # Encerra a sessão do webdriver
    driver.quit()

    # Cria um DataFrame Pandas com os dados extraídos
    catalago_kabum = pd.DataFrame(produtos)
    catalago_kabum.index.name = 'ID'

    # Salva os dados em um arquivo CSV
    catalago_kabum.to_csv(
        f'C:/Users/Renato/Desktop/Engenharia de dados/ETL/webscraping/excel_file/{item}_{data_atual}.csv',
        encoding='utf-8', sep=';')

# Itera sobre todas as categorias de hardware e executa o scraping
for tipo_produto in hardware:
    ws(tipo_produto)