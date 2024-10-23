import pickle
import os
from citations import scrape_dois, ads, pubmed, crossref, plots, publist
from tqdm import tqdm

# Scrape from Orcid
dois, name = scrape_dois.query_orcid('0000-0002-5074-7183')


# Load existing data
if os.path.exists('datadump.p'):
    papers = pickle.load(open("datadump.p", "rb"))
else:
    papers = {}


for doi in tqdm(dois):
    if doi not in papers.keys():
        papers[doi] = {'status': 'Missing'}

    # Scrape papers
    for source in ['ads', 'pubmed', 'crossref']:
        if papers[doi]['status'] == 'Missing':
            papers[doi] = eval(source+'.query_paper(doi)')

    # Scrape citations
    if papers[doi]['status'] != 'Missing':
        citations = eval(papers[doi]['source']+'.get_citations(doi)')
        for item in citations:
            if item not in papers[doi]['citations'].keys():
                # scrape new citations info
                info = eval(papers[doi]['source']+'.query_paper(item)')
                papers[doi]['citations'][item] = info
        # Prune obsolete citations
        keys = list(papers[doi]['citations'].keys())
        for item in keys:
            if item not in citations:
                papers[doi]['citations'].pop(item, None)


sorted_papers = sorted(papers.items(), key=lambda x: (
    x[1]['pubyear'], x[1]['pubmonth']), reverse=True)

papers = {k: v for k, v in sorted_papers}

# Save data
pickle.dump(papers, open("datadump.p", "wb"))


publist.to_screen(papers, name)
plots.make_plots(papers, name)
publist.make_publist(papers, name)
