import pandas as pd
import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import inspect
from sqlalchemy_utils import database_exists, create_database


def transformar_arquivo_csv(caminho_arquivo):
    try:
        # Lê o arquivo CSV
        df = pd.read_csv(caminho_arquivo, on_bad_lines='skip', sep=';', header=0, decimal=',')
        
        # Realiza as transformações necessárias
        # Por exemplo, define a coluna 'ID' como índice
        if 'ID' in df.columns:
            df.set_index('ID', inplace=True)
        
        df['Nome do produto'] = df['Descrição'].str.split(pat=',', n=1).str[0]
        df = df.reindex(columns=['Nome do produto', 'Descrição', 'Preço em R$'])
        df['Descrição'] = df.apply(lambda row: row['Descrição'].replace(row['Nome do produto'], '').strip(), axis=1)
        df['Preço em R$'] = df['Preço em R$'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
        df['Preço em R$'] = df['Preço em R$'].astype(float) / 100 * 100
        
        # Outras transformações podem ser adicionadas aqui
        
        return df
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV {caminho_arquivo}: {e}")
        return None

def extrar_arquivos():
    lista_df = {}  # Alteração aqui: agora vamos usar um dicionário para armazenar os DataFrames
    
    # Diretório onde estão os arquivos CSV
    diretorio = 'C:/Users\Renato/Desktop/Engenharia de dados/ETL/webscraping/excel_file'

    # Lista para armazenar os nomes dos arquivos CSV
    arquivos_csv = []

    # Iterar sobre todos os arquivos no diretório
    for arquivo in os.listdir(diretorio):
        # Verificar se o arquivo tem a extensão .csv
        if arquivo.endswith('.csv'):
            # Adicionar o nome do arquivo à lista
            arquivos_csv.append(arquivo)
                
    for tipo_produto in arquivos_csv:
        nome_tabela = tipo_produto.replace('.csv', '').replace('-', '_').replace('.', '_').replace(' ', '_')  # Limpar o nome do arquivo
        caminho_arquivo = f'{diretorio}/{tipo_produto}'
        lista_df[nome_tabela] = transformar_arquivo_csv(caminho_arquivo)
        
    return lista_df  # Retornar o dicionário com os DataFrames atribuídos aos nomes dos arquivos

# Chamada da função para extrair os arquivos e atribuir aos nomes correspondentes
dataframes = extrar_arquivos()


diretorio = 'C:/Users\Renato/Desktop/Engenharia de dados/ETL/webscraping/excel_file'
arquivos_csv = []
for arquivo in os.listdir(diretorio):
        # Verificar se o arquivo tem a extensão .csv
    if arquivo.endswith('.csv'):
            # Adicionar o nome do arquivo à lista
        arquivos_csv.append(arquivo[:-4])

def get_engine(user, passwd, host, port, db):
    url = f'postgresql://{user}:{passwd}@{host}:{port}/{db}'
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url, echo=True)
    return engine

hostname = 'localhost'
database = 'hardware'
username = 'postgres'
pwd = '503645'  # A senha deve ser uma string
port_id = 5432

engine = get_engine(username, pwd, hostname, port_id, database)

Base = declarative_base()

# Função para criar uma classe de tabela dinamicamente
def criar_classe_tabela(nome_tabela):
    class_name = nome_tabela.capitalize()
    return type(class_name, (Base,), {
        '__tablename__': nome_tabela,
        'id': Column(Integer, primary_key=True),
        'nome_produto': Column(String(255)),
        'descricao': Column(String(255)),
        'preco': Column(Float)
    })

# Criar as tabelas se não existirem
def criar_tabelas(engine):
    Base.metadata.create_all(engine)

# Chamar a função para criar as tabelas
criar_tabelas(engine)

Session = sessionmaker(bind=engine)
session = Session()

def adicionar_to_db(df, table_name):
    table_class = criar_classe_tabela(table_name)
    for index, row in df.iterrows():
        user = table_class(nome_produto=row['Nome do produto'], descricao=row['Descrição'], preco=row['Preço em R$'])
        session.add(user)

# lógica para dropar e criar a tabela se já existir
def adicionar_to_db_with_drop(df, table_name, engine):
    inspector = inspect(engine)
    if inspector.has_table(table_name):
        Base.metadata.tables[table_name].drop(engine)
    table_class = criar_classe_tabela(table_name)
    Base.metadata.tables[table_name].create(engine)
    for index, row in df.iterrows():
        user = table_class(nome_produto=row['Nome do produto'], descricao=row['Descrição'], preco=row['Preço em R$'])
        session.add(user)

for nome_tabela, df in dataframes.items():
    adicionar_to_db_with_drop(df, nome_tabela, engine)

session.commit()
session.close()
