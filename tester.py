import ezgmail, re, requests, time


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
sequencia = ['|', '/', '-', '\\']

with open('object.js', 'r') as f:
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', f.read())
    for i, link in enumerate(urls):
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

        print(sequencia[i % 4], end='\r')

outstring = formata(dicionario)

#print(outstring)
ezgmail.send('mendes.lnr@gmail.com','Relatório TJFacil',outstring)
