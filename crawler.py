#%%
from selenium import webdriver

driver = webdriver.Chrome('./chromedriver.exe')
driver.get('http://www4.pr.gov.br/escolas/frmPesquisaEscolas.jsp')

#%%
from bs4 import BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

links_redirects = []
for element in soup.find_all('td', attrs={'colspan':'2'}):
    onclick = element.get('onclick')
    if onclick:
        links_redirects.append(onclick.replace(')', ',"_self")'))
len(links_redirects)

#%%
from tqdm.notebook import tqdm 
import re 
import json 

def get_data():
    html = BeautifulSoup(driver.page_source, 'html.parser')
    data = {}
    
    data['nr'] = re.findall(r'NRE: (.+)', html.text)
    data['municipio'] = re.findall(r'Município: (.+)', html.text)
    data['dependencia_administrativa'] = re.findall(r'Dependência Administrativa: (.+)', html.text)
    data['compartilha_estrutura'] = re.findall(r'Compartilha a estrutura física com a escola: (.+)', html.text)
    
    data['nome'] = re.findall(r'Nome da Escola: (.+)', html.text)
    data['email'] = re.findall(r'Email: (.+)', html.text)
    data['endereco'] = re.findall(r'Endereço: (.+)', html.text)
    data['bairro'] = re.findall(r'Bairro: (.+)', html.text)
    data['cep'] = re.findall(r'Cep: (.+)', html.text)
    data['numero'] = re.findall(r'Número: (.+)', html.text)
    
    data['diretor'] = re.findall(r'Diretor: (.+)', html.text)
    data['secretario'] = re.findall(r'Secretário: (.+)', html.text)
    
    for key,value in data.items():
        data[key]=value[0] if value else None
    #print(json.dumps(data, indent=2))
    return data

import time 

datas = []
for redirect in tqdm(links_redirects):
    driver.execute_script(redirect)
    time.sleep(0.01)
    datas.append(get_data())

import pandas as pd
from csv import QUOTE_ALL

df = pd.DataFrame(datas)
df.to_csv('federal_contato.csv', index=False, sep=';', quoting=QUOTE_ALL)
