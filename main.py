#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
from datetime import date
import requests
from urllib import request, parse
from bs4 import BeautifulSoup
import tweepy
#from keys import *

auth = tweepy.OAuthHandler(os.environ.get("CONSUMER_KEY"), os.environ.get("CONSUMER_SECRET"))
auth.set_access_token(os.environ.get("ACCESS_TOKEN"), os.environ.get("ACCESS_TOKEN_SECRET"))

# Create API object
api = tweepy.API(auth)


regex_dolar = re.compile('(\d+)[.,](\d+)')
dolar_values = {}


def parse_dolar(val):
    match = regex_dolar.search(val)
    if (not match):
        return False
    else:
        dolar = float(match.group(1) + '.' + match.group(2))
        return dolar

def get_santander():
    with request.urlopen('https://banco.santanderrio.com.ar/exec/cotizacion/index.jsp') as rq:
        soup = BeautifulSoup(rq.read(), 'html.parser')
        dolar_compra = soup.find('td', string = 'Dólar').find_next_siblings()[0].string
        dolar_venta = soup.find('td', string = 'Dólar').find_next_siblings()[1].string
        return 'Compra: $' + str(parse_dolar(dolar_compra)) + ' Venta: $' + str(parse_dolar(dolar_venta))

def get_nacion():
    rq = requests.get('http://www.bna.com.ar/Personas/')
    soup = BeautifulSoup(rq.text, 'html.parser')
    dolar_compra = soup.find('table', 'table cotizacion').find('td', string = 'Dolar U.S.A').find_next_siblings()[0].string
    dolar_venta = soup.find('table', 'table cotizacion').find('td', string = 'Dolar U.S.A').find_next_siblings()[1].string
    return 'Compra: $' + str(parse_dolar(dolar_compra)) + ' Venta: $' + str(parse_dolar(dolar_venta))

def get_bbva():
    with request.urlopen('https://hb.bbv.com.ar/fnet/mod/inversiones/NL-dolareuro.jsp') as rq:
        soup = BeautifulSoup(rq.read(), 'html.parser')
        dolar_compra = soup.find('td', string = 'Dolar').find_next_siblings()[0].string
        dolar_venta = soup.find('td', string = 'Dolar').find_next_siblings()[0].string
        return 'Compra: $' + str(parse_dolar(dolar_compra)) + ' Venta: $' + str(parse_dolar(dolar_venta))

def get_bolsa():
    rq = requests.get('https://www.invertironline.com/mercado/cotizaciones?pais=Argentina&instrumento=Monedas&panel=Principales%20divisas&actualizar=true')
    soup = BeautifulSoup(rq.text, 'html.parser')
    match = re.compile('\Dólar Bolsa')
    tabla = soup.findAll('table')[0].findAll('tr')
    for item in tabla:
        data = item.find_all('td')
        if (match.search(data[0].text)) :
            dolar_compra = data[1].text
            dolar_venta = data[2].text
    return 'Compra: $' + str(parse_dolar(dolar_compra)) + ' Venta: $' + str(parse_dolar(dolar_venta))

def get_galicia():
    url = 'https://www.bancogalicia.com/cotizacion/cotizar?currencyId=02&quoteType=SU&quoteId=999'
    rs = json.loads(requests.get(url).text)
    dolar_compra = rs['buy']
    dolar_venta = rs['sell']
    return 'Compra: $' + str(parse_dolar(dolar_compra)) + ' Venta: $' + str(parse_dolar(dolar_venta))

def get_patagonia():
    with request.urlopen('https://ebankpersonas.bancopatagonia.com.ar/eBanking/usuarios/cotizacionMonedaExtranjera.htm') as rq:
        soup = BeautifulSoup(rq.read(), 'html.parser')
        dolar_compra = soup.find('td', string='DOLARES').find_next_siblings()[0].string
        dolar_venta = soup.find('td', string='DOLARES').find_next_siblings()[1].string
        return 'Compra: $' + str(parse_dolar(dolar_compra)) + ' Venta: $' + str(parse_dolar(dolar_venta))

def get_dolarblue():
    r = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
    if r.status_code == 200:
        json_data = json.loads(r.text)
        dolar_compra = json_data[1]['casa']['compra']
        dolar_venta = json_data[1]['casa']['venta']
        return 'Compra: $' + str(parse_dolar(dolar_compra)) + ' Venta: $' + str(parse_dolar(dolar_venta))

def get_contadoconliqui():
    r = requests.get('https://www.dolarsi.com/api/api.php?type=valoresprincipales')
    if r.status_code == 200:
        json_data = json.loads(r.text)
        dolar_compra = json_data[3]['casa']['compra']
        dolar_venta = json_data[3]['casa']['venta']
        return 'Compra: $' + str(parse_dolar(dolar_compra)) + ' Venta: $' + str(parse_dolar(dolar_venta))

def get_riesgopais():
    with request.urlopen('https://www.rava.com/empresas/precioshistoricos.php?e=RIESGO%20PAIS') as rq:
        soup = BeautifulSoup(rq.read(), 'html.parser')
        list = soup.find('tr', 'ci')
        for item in list:
            if (item.string != '0'):
                riesgo_pais = item.string
        return riesgo_pais 

dolar_colores =  [
    ('Oficial', get_nacion),
    ('Blue', get_dolarblue),
    ('Contado con Liqui', get_dolarblue),
    ('Bolsa', get_bolsa) ]



bancos = [
    ('Santander', get_santander),
    ('BBVA', get_bbva),
    ('Galicia', get_galicia),
    ('Patagonia', get_patagonia),
    ('Riesgo Pais',get_riesgopais)
]

def dolar_bancos():
    message = ''
    for banco, getter in bancos: 
        try:
            value = getter()
            message += '\n' + banco + ': ' + value 
        except:
            print('Error obteniendo {nombre}'.format(nombre=banco))
    if (len(message) == 3):
        print("\nNo se pudo obtener ningún valor")
    return message

def dolar_colores_list():
    message = ''
    for tipodolar, getter in dolar_colores: 
        try:
            value = getter()
            message += '\n' + tipodolar + ': ' + value 
        except:
            print('Error obteniendo {nombre}'.format(nombre=tipodolar))
    if (len(message) == 3):
        print("\nNo se pudo obtener ningún valor")
    return message

api.update_status(dolar_colores_list())
api.update_status(dolar_bancos())