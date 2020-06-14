# Importando libs

import bs4
from bs4 import BeautifulSoup

import selenium
from selenium import webdriver

import numpy as np

import pandas as pd

import matplotlib

import matplotlib.pyplot as plt

from collections import Counter

# Com o NLTK fazemos Processamento de Linguagem Natural
import nltk

# Temos que fazer o download do dicionário e demais pacotes do NLTK
nltk.download('all')

# Tokenização é o processo de quebrar uma sentença em palavras, por exemplo.
# Essa tarefa faz parte do processamento de linguagem natural. 
# Vamos importar a função word_tokenize.
from nltk import word_tokenize

# As stopwords são palavras comuns, como artigos, advérbios ou conjunções.
# As stopwords devem ser removidas no processamento de linguagem natural.
# Vamos importar a função stopwords.
from nltk.corpus import stopwords

# Cria o driver de conexão. Será aberta outra janela do navegador. Não feche-a e mantenha aberta durante a extração.
driver = webdriver.Chrome("./chromedriver")

# Cria o dataframe para receber os dados
dados = pd.DataFrame(columns = ["Titulo", "Localidade", "Empresa", "Salario", "Tipo_Pesquisa", "Desc"])

# Abre a conexão com o site e faz a pesquisa
driver.get("https://www.indeed.com.br/jobs?q=data+science&l=brasil")
driver.implicitly_wait(15)

# Gravamos o resultado do scraping
resultado = driver.find_elements_by_class_name("result")

# Temos apenas os elementos web. Precisamos agora extrair o texto desses elementos
print(resultado)

# interar pelos resultados do scraping e extrari dados nas tags HTML do nosso interesse
for vaga in resultado:
    
    # Primeiro coletamos o elemento HTML interno
    result_html = vaga.get_attribute('innerHTML')
    
    # Fazemos então o parser do código HTML
    soup = BeautifulSoup(result_html, 'html.parser')
    
    # Buscamos as tags para análise. 
    # Usaremos blocos try/except para evitar erros na execução, no caso de ua informação não estar disponível na vaga
    
    # Título da vaga
    try:
        title = soup.find("a", class_ = "jobtitle").text.replace('\n', '')
    except:
        title = 'None'
    
    # Localidade
    try:
        location = soup.find(class_ = "location").text
    except:
        location = 'None'
    
    # Empresa
    try:
        company = soup.find(class_ = "company").text.replace('\n', '').strip()
    except:
        company = 'None'
    
    # Salário
    try:
        salary = soup.find("a", class_ = "salary").text.replace('\n', '').strip()
    except:
        salary = 'None'
    
    # Tipo de pesquisa (orgânica ou patrocinada)
    try:
        sponsored = soup.find("a", class_ = "sponsoredGray").text
        sponsored = "Sponsored"
    except:
        sponsored = 'Organic'
        
    # Aqui buscamos o sumário
    sum_div = vaga.find_elements_by_class_name("summary")[0]
    sum_div.click()
    
    # Descrição da vaga
    job_desc = driver.find_element_by_id('vjs-desc').text
    
    # Gravamos o resultado em nosso dataframe
    dados = dados.append({"Titulo":title, 
                          "Localidade":location, 
                          "Empresa":company, 
                          "Salario":salary, 
                          "Tipo_Pesquisa":sponsored, 
                          "Desc":job_desc}, 
                         ignore_index = True)

# Visualizamos os dados
dados.head()

# Salvamos os dados em disco
dados.to_csv('resultado/dados.csv', encoding = "utf-8", index = False)
