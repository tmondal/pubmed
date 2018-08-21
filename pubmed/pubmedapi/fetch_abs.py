import requests

def fetch_data(query,gene,n):
    
    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&api_key=947c1845e9a006cd589f251e11def613e308&term={}&reldate=60&datetype=edat&retmax={}&retmode=json'
    res = requests.get(url.format(query,n)).json()

    # # api call with proxy
    # url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&api_key=947c1845e9a006cd589f251e11def613e308&term={}&reldate=60&datetype=edat&retmax=1&retmode=json'
    # res = requests.get(url.format(query),proxies=proxy_dict).json()

    idlist = res['esearchresult']['idlist']
    # print(idlist)
    # for id in idlist:
    #     print(id)
    #     abstracturl = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&api_key=947c1845e9a006cd589f251e11def613e308&id={}&retmode=text&rettype=abstract'
    #     idabstract = requests.get(abstracturl.format(id))
    #     # print(idabstract.text)
    #     abstract.append(idabstract.text)
    #     # print(abstract)