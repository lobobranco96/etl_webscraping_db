# Processo de ETL: Extração, Transformação e Load de Dados da Kabum para o Banco de Dados
Este projeto consiste em um processo de ETL (Extração, Transformação e Load) para coletar informações sobre diferentes tipos de hardware do site da Kabum (https://www.kabum.com.br/) e armazená-las em um banco de dados PostgreSQL.

# Bibliotecas Utilizadas
- selenium: Utilizada para automatizar a navegação web e a extração de dados do site da Kabum.
- webdriver_manager: Utilizada para gerenciar e instalar automaticamente o driver do navegador Chrome.
- BeautifulSoup: Utilizada para fazer a análise de HTML e a extração dos dados relevantes da página web.
- pandas: Utilizada para manipulação e transformação dos dados.
- datetime: Utilizada para obter a data atual para inclusão no nome dos arquivos CSV.
- sqlalchemy: Utilizada para interagir com o banco de dados PostgreSQL.
  
# Funcionalidades do Script
- O processo de ETL realizado pelo script consiste nas seguintes etapas:

# Extração de Dados:

- Define URLs para diferentes tipos de hardware disponíveis no site da Kabum.
- Configura o Selenium para usar o driver do Chrome em modo headless (sem interface gráfica).
- Navega pelas páginas do site da Kabum, extrai informações como marca e preço dos produtos e armazena em um dicionário.
- Salva os dados extraídos em arquivos CSV.
  
# Transformação de Dados:

- lê os arquivos CSV com os dados extraídos.
- Realiza transformações nos dados, como limpeza, formatação e criação de novas colunas.
  
# Load de Dados no Banco de Dados:

- Conecta-se ao banco de dados PostgreSQL.
- Cria tabelas dinamicamente com base nos arquivos CSV de entrada.
- Carrega os dados transformados nas tabelas do banco de dados.
  
# Instruções de Uso
- Certifique-se de ter todas as dependências instaladas (consulte a seção de Bibliotecas Utilizadas).
- Execute o script Python fornecido neste repositório.
- Os dados serão extraídos, transformados e carregados no banco de dados PostgreSQL especificado no script.
  
# Notas
- É importante respeitar os termos de uso do site da Kabum ao realizar web scraping e não sobrecarregar o servidor com solicitações excessivas.
- Este script foi desenvolvido apenas para fins educacionais e de demonstração. Se você planeja usar web scraping em um ambiente de produção, é importante garantir que esteja em conformidade com as políticas do site alvo.
  
# Autor
Este script foi desenvolvido por [lobobranco96]. Para perguntas ou feedback, entre em contato através do [e-mail ou perfil do GitHub].
