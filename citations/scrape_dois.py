import requests
import xml.etree.ElementTree as ET


def query_orcid(orcid):
    ''' Get name and dois from ORCID
        First entry of dois is the name of the ORCID ID owner
    '''
    query_url = "https://pub.orcid.org/"+orcid+"/person"
    response = requests.get(query_url)
    lines = response.text.split('\n')
    for line in lines:
        if "family-name" in line:
            name = [line.split("<personal-details:family-name>")[
                1].split("</personal-details:family-name>")[0]]

    dois = []
    query_url = "https://pub.orcid.org/"+orcid+"/works"
    response = requests.get(query_url)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        groups = root.findall('.//{http://www.orcid.org/ns/activities}group')
        for group in groups:
            worktype = group.find('.//{http://www.orcid.org/ns/work}type').text
            title = group.find('.//{http://www.orcid.org/ns/common}title').text
            if worktype == 'journal-article' and 'Author Correction' not in title:
                ids = group.findall(
                    './/{http://www.orcid.org/ns/common}external-id')
                doi = ''
                for id in ids:
                    if id.find('.//{http://www.orcid.org/ns/common}external-id-type').text == 'doi':
                        doi = id.find(
                            './/{http://www.orcid.org/ns/common}external-id-value').text
                if doi == '':
                    print(f"No doi found for {title}")
                else:
                    dois.append(doi)

    dois = set(dois)

    return dois, name[0]
