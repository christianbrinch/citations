import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MaxNLocator
import numpy as np
from datetime import date

NOW = date.today().year+date.today().month/12.


def setup_axis(fig_nr, **params):
    ''' Setup axis based on parameters sent from plot functions
    '''
    _ = plt.figure(fig_nr)
    axe = plt.subplot(111)
    axe.set_xlim(params['xlim'][0], params['xlim'][1])
    axe.set_xlabel(params['xlabel'])
    if 'xticks' in params:
        plt.xticks(params['xticks'])
    if 'ylim' in params:
        axe.set_ylim(params['ylim'][0], params['ylim'][1])
    axe.set_ylabel(params['ylabel'])
    axe.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    axe.yaxis.set_major_locator(MaxNLocator(integer=True))
    axe.minorticks_on()
    if 'minor_locator' in params:
        axe.xaxis.set_minor_locator(AutoMinorLocator(12))
    return axe


def hindex_calc(papers):
    ''' Calculate the h-index and the h5-index (h-index over the last 5 years)
    '''
    start = float(min([papers[i]['pubyear'] for i in papers]))
    months = int(12*(NOW-start))

    citation_hist = {}
    for doi in papers:
        citation_hist[doi] = np.zeros(months)
        for item in papers[doi]['citations']:
            pubmonth = int(round(((float(papers[doi]['citations'][item]['pubyear']) +
                                   (float(papers[doi]['citations'][item]['pubmonth'])-1)/12.) -
                                  start)*12, 0))
            citation_hist[doi][pubmonth] += 1

    hidx = []
    h5idx = []
    for i in range(months):
        cs_month = sorted([np.cumsum(citation_hist[doi])[i]
                          for doi in citation_hist], reverse=True)
        hidx.append(int([i for i, idx in enumerate(cs_month) if i >= idx][0]))

        cs_month = sorted([np.cumsum(citation_hist[doi][max(0, i-60):])[min(i, 60)]
                          for doi in citation_hist], reverse=True)
        h5idx.append(int([i for i, idx in enumerate(cs_month) if i >= idx][0]))

    return hidx, h5idx


def citations_in_time(papers, start, fig_nr):
    ''' Plot citations in time
    '''
    tc = sum([len(papers[doi]['citations']) for doi in papers])

    axis_params = {'xlim': (start-1., NOW+2.),
                   'xlabel': 'Year',
                   'ylim': (0, 1.2*tc),
                   'ylabel': 'Number of citations'}
    axe = setup_axis(fig_nr, **axis_params)

    months = int(12*(NOW-start))
    citation_hist = np.zeros(months)
    for doi in papers:
        for item in papers[doi]['citations']:
            pubmonth = int(round(((float(papers[doi]['citations'][item]['pubyear'])+(
                float(papers[doi]['citations'][item]['pubmonth'])-1)/12.)-start)*12, 0))
            citation_hist[min(pubmonth, len(citation_hist)-1)] += 1
    axe.plot(start+np.arange(months)/12.,
             np.cumsum(citation_hist), alpha=0.8, lw=1.8)

    for step in 1000*(np.arange(int(tc/1000))+1):
        axe.step([start-1., NOW+2.], [step, step],
                 '--', alpha=0.6, color='grey')


def citations_per_month(papers, start, fig_nr):
    ''' Plot citations per month
    '''

    axis_params = {'xlim': (start-1., NOW+2.),
                   'xlabel': 'Year',
                   'xticks': np.arange(start-1, int(NOW)+2, 1),
                   'ylabel': 'Citations per month',
                   'minor_locator': 12}
    axe = setup_axis(fig_nr, **axis_params)

    months = int(12*(NOW-start))
    citation_hist = np.zeros(months)
    for doi in papers:
        for item in papers[doi]['citations']:
            pubmonth = int(round((((float(papers[doi]['citations'][item]['pubyear'])+(
                float(papers[doi]['citations'][item]['pubmonth'])-1)/12.)-start)*12), 0))
            citation_hist[min(pubmonth, len(citation_hist)-1)] += 1

    axe.bar(start+np.arange(months)/12, citation_hist,
            width=1/12., align='edge', facecolor='seagreen')


def hindex_in_time(papers, start, fig_nr):
    ''' Plot h-index in time
    '''

    hindex, h5index = hindex_calc(papers)
    axis_params = {'xlim': (start-1., NOW+2.),
                   'xticks': np.arange(start-1, int(NOW)+2, 1),
                   'xlabel': 'Year',
                   'ylabel': 'h-index'}
    axe = setup_axis(fig_nr, **axis_params)
    axe.plot(start+np.arange(len(hindex)) /
             12., hindex, color='steelblue', lw=1.8)

    x_axis = np.arange(len(hindex))/12. + start
    axe.plot(x_axis, x_axis-start, color='black', lw=1.8, alpha=0.6)
    axe.plot(x_axis, 2*(x_axis-start), color='black', lw=1.8, alpha=0.6)
    axe.plot(start+np.arange(len(h5index)) /
             12., h5index, color='maroon', lw=1.8)
    axe.plot(x_axis, (hindex[-1]/(NOW-start)) *
             (x_axis-start), '--', color='goldenrod', lw=1.8)

    x_short = np.array([NOW-3., NOW])
    axe.plot(x_short, (hindex[-1]-hindex[-36])/3.*(x_short-(NOW-3.)) +
             hindex[-36], '--', color='seagreen', lw=1.8)

    print("h-index: {0:d}".format(hindex[-1]))
    print("h-index slope: {0:0.2f}".format(hindex[-1]/(NOW-start)))
    print("h5-index: {0:d}".format(h5index[-1]))


def citations_per_paper_in_time(papers, name, start, fig_nr):
    ''' Plot citations per paper in time
    '''

    axis_params = {'xlim': (-1, NOW+1-start),
                   'xlabel': 'Years after publication',
                   'ylabel': 'Citations'}
    axe = setup_axis(fig_nr, **axis_params)

    for doi in papers:
        if name in papers[doi]['authors'][0]:
            color = 'maroon'
        else:
            color = 'steelblue'

        ppubmonth = float(papers[doi]['pubyear']) + \
            (float(papers[doi]['pubmonth'])-1)/12
        months = int(12*(NOW-ppubmonth)+1)
        citation_hist = np.zeros(months)
        for item in papers[doi]['citations']:
            pubmonth = min(float(papers[doi]['citations'][item]['pubyear'])+(
                float(papers[doi]['citations'][item]['pubmonth'])-1)/12., NOW)-ppubmonth

            citation_hist[max(0, int(round(12*pubmonth, 0)))] += 1

        axe.plot(np.arange(months)/12.,
                 np.cumsum(citation_hist), alpha=0.8, lw=1.8, color=color)

    x_axis = np.arange(int((NOW-start)*12.))/12.
    axe.plot(x_axis, 12.*x_axis, '--', color='black', alpha=0.6)


def citations_per_paper(papers, name, fig_nr):
    ''' Plot citations per paper
    '''

    axis_params = {'xlim': (0, len(papers)),
                   'xlabel': '',
                   'xticks': np.arange(0, len(papers), 1.)+0.4,
                   'ylabel': 'Citations'}
    axe = setup_axis(fig_nr, **axis_params)

    hindex, _ = hindex_calc(papers)
    sorted_papers = sorted(
        papers.items(), key=lambda x: len(x[1]['citations']), reverse=True)
    papers = {k: v for k, v in sorted_papers}

    axe.minorticks_off()

    axe.set_xticklabels([papers[doi]['title'][0:20] for doi in papers], rotation=45,
                        rotation_mode="anchor", ha="right", fontsize=6)

    cites = list(map(int, [len(papers[doi]['citations'])
                           for doi in papers]))

    axe.bar(np.arange(len(papers)), cites,
            color=['maroon' if name in papers[doi]['authors'][0] else 'steelblue' for doi in papers], align='edge')
    axe.plot([0, len(papers)],
             [hindex[-1], hindex[-1]], '--', color='black', alpha=0.6)
    axe.text(len(papers)-5, hindex[-1]+2, 'h-index')


def publications_in_time(papers, start, fig_nr):
    ''' Plot publication history per year
    '''

    axis_params = {'xlim': (start-1., NOW+2.),
                   'xlabel': 'Year',
                   'xticks': np.arange(start-1, int(NOW)+2, 1),
                   'ylabel': 'Number of publications per year'}
    axe = setup_axis(fig_nr, **axis_params)

    publications = [int(papers[doi]['pubyear']) for doi in papers]
    total_years = (int(NOW+2)-int(start-1))

    axe.hist(publications, bins=total_years, range=(
        int(start-1), int(NOW)+2), facecolor='seagreen')


def make_plots(papers, name):
    start = float(min([papers[i]['pubyear'] for i in papers]))
    citations_in_time(papers, start, 1)
    citations_per_month(papers, start, 2)
    hindex_in_time(papers, start, 3)
    citations_per_paper_in_time(papers, name, start, 4)
    citations_per_paper(papers, name, 5)
    publications_in_time(papers, start, 6)
