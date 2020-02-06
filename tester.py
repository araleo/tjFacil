#!/usr/bin/env python3

import ezgmail, re, requests, time
from datetime import date


def formata(dicionario):
    outstring = ''
    for nome, conj in dicionario.items():
        outstring += f"""
{nome}:

"""
        for item in conj:
            outstring += f"""
{item}

"""
    return outstring


dicionario = {'erros': set(), 'timeouts': set(), 'ssl_error': set(), 'connection_timeout': set(), 'connection_error': set()}

with open('/home/pi/tjFacil/object.js', 'r') as f:
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', f.read())
    for link in urls:
        try:
            res = requests.get(link, timeout=5)
            if res.status_code != requests.codes.ok:
                dicionario['erros'].add(link)
        except requests.exceptions.ReadTimeout:
            dicionario['timeouts'].add(link)
        except requests.exceptions.SSLError:
            dicionario['ssl_error'].add(link)
        except requests.exceptions.ConnectTimeout:
            dicionario['connection_timeout'].add(link)
        except requests.exceptions.ConnectionError:
            dicionario['connection_error'].add(link)

outstring = formata(dicionario)

dia = date.today().strftime('%d%m%Y')
nome = f"/home/pi/tjFacil/relatorios/relatoriotjfacil{dia}.txt"

f_saida = open(nome,'w')
f_saida.write(outstring)
f_saida.close()

#print(outstring)
ezgmail.send('mendes.lnr@gmail.com','Relatório TJFácil',outstring)
