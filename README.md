# Web Scraping do Site Kabum e Armazenamento em Arquivos CSV
Este projeto consiste em um script Python para realizar web scraping do site da Kabum (https://www.kabum.com.br/) em busca de informações sobre diferentes tipos de hardware, como SSDs, coolers, fontes, placas de vídeo, etc.
Os dados coletados são então armazenados em arquivos CSV para posterior análise e processamento.

# Bibliotecas Utilizadas
- selenium: Utilizada para automatizar a navegação web e a extração de dados do site da Kabum.
- webdriver_manager: Utilizada para gerenciar e instalar automaticamente o driver do navegador Chrome.
- BeautifulSoup: Utilizada para fazer a análise de HTML e a extração dos dados relevantes da página web.
- pandas: Utilizada para manipulação e armazenamento de dados em estrutura de DataFrames.
-  datetime: Utilizada para obter a data atual para inclusão no nome dos arquivos CSV.
  
# Funcionalidades do Script
 O script realiza as seguintes tarefas:

- Definição de URLs: Define URLs para diferentes tipos de hardware disponíveis no site da Kabum.
- Configuração do WebDriver: Configura o Selenium para usar o driver do Chrome em modo headless (sem interface gráfica).
- Extração de Dados: Navega pelas páginas do site da Kabum, extrai informações como marca e preço dos produtos e armazena em um dicionário.
- Armazenamento em Arquivos CSV: Converte os dados extraídos para um DataFrame do Pandas e os salva em arquivos CSV, com o nome do arquivo contendo o tipo de hardware e a data da extração.

# Instruções de Uso
- Certifique-se de ter todas as dependências instaladas (consulte a seção de Bibliotecas Utilizadas).
- Execute o script Python fornecido neste repositório.
- Os arquivos CSV contendo os dados extraídos serão salvos no diretório especificado no script.
  
# Notas
É importante respeitar os termos de uso do site da Kabum ao realizar web scraping e não sobrecarregar o servidor com solicitações excessivas.
Este script foi desenvolvido apenas para fins educacionais e de demonstração. Se você planeja usar web scraping em um ambiente de produção, é importante garantir que esteja em conformidade com as políticas do site alvo.
Autor
Este script foi desenvolvido por [lobobranco96]. Para perguntas ou feedback, entre em contato através do [e-mail ou perfil do GitHub].
