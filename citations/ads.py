import requests


def query_paper(doi):
    url = "https://api.adsabs.harvard.edu/v1/search/query"
    headers = {
        'Authorization': 'Bearer:OnVZIdDD8oGy11bLaCnLZlBbbkNfKU1k0jd8FQ6L'}

    params = {'q': '\"'+doi+'\"',
              'wt': 'json',
              'fl': 'pubdate, title, bibcode, author, pub, issue, volume, page'}

    response = requests.get(url, headers=headers, params=params).json()

    paper = {}
    if response['response']['numFound'] > 0:
        paper['title'] = response['response']['docs'][0]['title'][0]
        paper['authors'] = [i for i in response['response']['docs'][0]['author']]
        paper['pubyear'] = response['response']['docs'][0]['pubdate'][:4]
        paper['pubmonth'] = response['response']['docs'][0]['pubdate'][5:7]
        paper['source'] = 'ads'
        paper['journal'] = response['response']['docs'][0]['pub']
        if 'volume' in response['response']['docs'][0].keys():
            paper['volume'] = response['response']['docs'][0]['volume']
        else:
            paper['volume'] = ''
        if 'issue' in response['response']['docs'][0].keys():
            paper['issue'] = response['response']['docs'][0]['issue']
        else:
            paper['issue'] = ''
        if 'page' in response['response']['docs'][0].keys():
            paper['pages'] = response['response']['docs'][0]['page'][0]
        else:
            paper['page'] = ''
        paper['citations'] = {}
        paper['status'] = 'Scraped'
    else:
        paper['status'] = 'Missing'
    return paper


def get_citations(doi):
    url = "https://api.adsabs.harvard.edu/v1/search/query"
    headers = {
        'Authorization': 'Bearer:OnVZIdDD8oGy11bLaCnLZlBbbkNfKU1k0jd8FQ6L'}

    params = {'q': '\"'+doi+'\"',
              'wt': 'json',
              'fl': 'citation'}

    response = requests.get(url, headers=headers, params=params).json()

    if response['response']['numFound'] > 0:
        if 'citation' in response['response']['docs'][0].keys():
            citations = response['response']['docs'][0]['citation']
        else:
            citations = []
    else:
        citations = []

    return citations
