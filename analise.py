import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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

# Carregamos o dataset
df = pd.read_csv("resultado/dados.csv", encoding = "utf-8")

# Visualizamos os dados
print(df.head())

# Tarefa 1: Qual o tipo de vaga mostrado na pesquisa, orgânica ou patrocinada?
print('Qual o tipo de vaga mostrado na pesquisa, orgânica ou patrocinada?')
print(df["Tipo_Pesquisa"].value_counts())


# Tarefa 2: 'Quais empresas tem o maior número de vagas listadas?'
grupo1 = df.groupby("Empresa").count()["Titulo"].sort_values(ascending = False)[:20]
print('Quais empresas tem o maior número de vagas listadas?')
print(grupo1.head(5))

# Plotando
grupo1.plot(kind = "bar", figsize = (18,6), color = "green", rot = 60)


# Tarefa 3: Qual localidade tem o maior número de vagas listadas?
# Agrupando Localidades
grupo2 = df.groupby("Localidade").count()["Titulo"].sort_values(ascending = False)[:20]
print('Qual localidade tem o maior número de vagas listadas?')
print(grupo2.head())
# Plotando
grupo2.plot(kind = "bar", figsize = (18,6), color = "blue", rot = 30)

# Tarefa 4: Quais os skills mais comuns nas descrições das vagas?

# Função de limpeza dos dados
def elimina(desc):
    desc = word_tokenize(desc)
    desc = [word.lower() for word in desc if word.isalpha() and len(word) > 2]
    desc = [word for word in desc if word not in stop_words_pt]
    desc = [word for word in desc if word not in stop_words_en]
    return desc

# Lista de StopWords em português
stop_words_pt = stopwords.words('portuguese')

# Lista de StopWords em português
stop_words_en = stopwords.words('english')

# Limpando as descrição da vaga
desc_vagas = df["Desc"].apply(elimina)

# Exibindo as 10 primeiras vagas limpas
print(desc_vagas.head(10))

# Vamos conta as descrições das vagas
desc_itens = desc_vagas.apply(Counter).sum().items()

# ORdenando as Vagas
desc_itens = sorted(desc_itens, key = lambda kv: kv[1], reverse = True)

# Cria Série
desc_itens_serie = pd.Series({k: v for k, v in desc_itens})

# Exibindo os 10 primeiros
print(desc_itens_serie.head(10))

# Vamos criar uma lista de skills e pesquisar como eles aparecem nas descrições das vagas
# Usamoas as palavras em minúsculo pois ao limpar os dados convertemos tudo para minúsculo
skills = ["python", "statistics", "analytics", "business", "projects", "develop"]

# Filtramos a série com os skills
filtro_skills = desc_itens_serie.filter(items = skills)

# Plotar
filtro_skills.plot(kind = 'bar', figsize = (18,6), color = "magenta", rot = 30)

