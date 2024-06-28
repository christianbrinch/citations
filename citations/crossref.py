import requests


def query_paper(doi):
    url = f"https://api.crossref.org/works/{doi}"

    response = requests.get(url)
    paper = {}
    if response.status_code == 200:
        data = response.json()
        paper['title'] = data['message']['title'][0]
        paper['first_author'] = data['message']['author'][0]['family']
        paper['authors'] = [i['family']+' '+i['given'][0]
                            for i in data['message']['author']]
        paper['pubyear'] = str(data['message']['created']['date-parts'][0][0])
        paper['pubmonth'] = str(data['message']['created']
                                ['date-parts'][0][1]).zfill(2)
        if len(data['message']['short-container-title']) > 0:
            paper['journal'] = data['message']['short-container-title'][0]
        else:
            paper['journal'] = 'N/A'
        if 'volume' in data['message'].keys():
            paper['volume'] = data['message']['volume'][0]
        else:
            paper['volume'] = ''
        paper['issue'] = ''
        paper['pages'] = ''
        paper['source'] = 'crossref'
        paper['citations'] = {}
        paper['status'] = 'Scraped'
    else:
        paper['status'] = 'Missing'

    return paper


def get_citations(doi):
    return []
