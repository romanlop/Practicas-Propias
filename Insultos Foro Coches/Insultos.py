#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 18 19:35:37 2019

@author: Ruman.
Acceso a ForoCoches para buscar insultos.
"""

import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
import pandas as pd
import requests
import urllib.request
import time
from bs4 import BeautifulSoup

# Importamos uno de los modelos en castellano -> es_core_news_sm 10MB; es_core_news_md -> 65MB
nlp = spacy.load('es_core_news_sm')

#cargamos el listado de insultos
insultos = pd.read_csv("insultos.csv",sep='\s+')

#Ver https://spacy.io/api/language#pipe para entender nlp.pipe
#Incorporamos los insultos a nuestro idioma.
insultos_patterns = list(nlp.pipe(insultos['Insultos']))

#Añadimos nuestros inslutos al matcher
matcher = PhraseMatcher(nlp.vocab)
matcher.add("INSULTO", None, *insultos_patterns)

# Definimos un paso adicional para nuestra cadena de procesamiento
def detector_insultos(doc):
    # Aplicamos el matcher
    matches = matcher(doc)
    # Create a Span for each match and assign the label 'INSULTO'
    #spans = [Span(doc, start, end, label="INSULTO") 
    label = nlp.vocab.strings["INSULTO"]
    spans = [Span(doc, start, end, label=label) for match_id, start, end in matches]
    # Overwrite the doc.ents with the matched spans
    doc.ents = spans
    return doc

"""
# Lo vamos a meter de último
nlp.add_pipe(detector_insultos, name="detector",after="ner")
print(nlp.pipe_names)


doc = nlp(u"Esto es una frase. Cabrón, hijo de puta, puta , Puta, Marica, Arrastracueros Zurcefrenillos asdasd ciruelossw ")
print([(ent.text, ent.label_) for ent in doc.ents])
"""

#Accedemos a ForoCoches y obtenemos los links de la página principal
base_url = 'https://www.forocoches.com/'
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")
list_links = []

for a in soup.find_all('a', href=True, attrs = {"class": "texto"}):
    #print ("Found the URL:", a['href'])
    list_links.append(a['href'])
    

contenido = []    
for i in range(0,1):
    #response = requests.get(base_url+list_links[i])
    response = requests.get('https://www.forocoches.com/foro/showthread.php?t=7190636')
    soup = BeautifulSoup(response.text, "html.parser")
    contenido.append(soup)
    time.sleep(1) #tiempo en segundos -> para no saturar la web.
    #print(contenido[i])


divs=contenido[0].find_all('div, attrs = {"id": "HOTWordsTxt"}')
print(divs)

    
    #, attrs={'style': 'word-wrap:break-word;'}
"""
#Nos quedamos solo con los Links que nos Interesan
links=soup.findAll('a', attrs = {"class": "texto"})
list_links = []
word = 'rel="nofollow">»</a>'
for i in range(len(links)):
    if word not in str(links[i]).split():
        list_links.append(str(links[i]))
"""
        



