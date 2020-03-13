import os
import re
import json
from datetime import date
import requests
from urllib import request, parse
from bs4 import BeautifulSoup

regex_dolar = re.compile('(\d+)[.,](\d+)')
dolar_values = {}


def parse_dolar(val):
    match = regex_dolar.search(val)
    if (not match):
        return False
    else:
        dolar = float(match.group(1) + '.' + match.group(2))
        return dolar



rq = requests.get('https://www.invertironline.com/mercado/cotizaciones?pais=Argentina&instrumento=Monedas&panel=Principales%20divisas&actualizar=true')
soup = BeautifulSoup(rq.text, 'html.parser')
match = re.compile('\Dólar Bolsa')
tabla = soup.findAll('table')[0].findAll('tr')
for item in tabla:
    data = item.find_all('td')
    if (match.search(data[0].text)) :
        dolar_compra = data[1].text
        dolar_venta = data[2].text

print('Compra: $' + str(parse_dolar(dolar_compra)) + ' Venta: $' + str(parse_dolar(dolar_venta)))