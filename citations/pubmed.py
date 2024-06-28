
import requests
import xml.etree.ElementTree as ET


def get_pmid_from_doi(doi):
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={doi}[DOI]'
    response = requests.get(url)
    try:
        root = ET.fromstring(response.content)
        pmid = root.find('.//Id').text
        return pmid
    except:
        return None


def query_paper(pmid):
    month = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
             'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

    # if slash in pmid, then pmid is a doi and needs to be converted.
    if '/' in pmid:
        pmid = get_pmid_from_doi(pmid)
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=xml'
    response = requests.get(url)
    paper = {}
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        docsum = root.find('.//DocSum')
        if docsum is not None:
            pubdate = docsum.find('.//Item[@Name="PubDate"]').text
            paper['pubyear'] = pubdate[:4]
            if len(pubdate) >= 9:
                if pubdate[5:8] in month.keys():
                    paper['pubmonth'] = month[pubdate[5:8]]
                else:
                    paper['pubmonth'] = '01'
            else:
                paper['pubmonth'] = '01'
            paper['title'] = docsum.find('.//Item[@Name="Title"]').text
            paper['authors'] = [i.text for i in docsum.findall(
                './/Item[@Name="Author"]')]
            paper['journal'] = docsum.find('.//Item[@Name="Source"]').text
            paper['volume'] = docsum.find('.//Item[@Name="Volume"]').text
            paper['issue'] = docsum.find('.//Item[@Name="Issue"]').text
            paper['pages'] = docsum.find('.//Item[@Name="Pages"]').text
            paper['source'] = 'pubmed'
            paper['citations'] = {}
            paper['status'] = 'Scraped'
        else:
            paper['status'] = 'Missing'
    else:
        paper['status'] = 'Missing'

    return paper


def get_citations(doi):
    pmid = get_pmid_from_doi(doi)
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&id={pmid}&cmd=neighbor&linkname=pubmed_pubmed_citedin'
    response = requests.get(url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        citations = []
        for link in root.findall('.//Link'):
            citations.append(link.find('.//Id').text)
        return citations
    else:
        return []
