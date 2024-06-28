import math
from citations import plots


def to_screen(papers, name):
    # Print report to screen
    print()
    print(f"| DOI{' '*25}| Title{' '*12}| First author    "
          f"| Year | Month | Journal{' '*24}| Source    | #citations |")
    print(f"+{'-'*29}+{'-'*18}+{'-'*17}+{'-'*6}+{'-'*7}+{'-'*32}+{'-'*11}+{'-'*12}+")
    for doi in papers:
        print(f"| {doi[:27]:27} | {papers[doi]['title'][:16]} "
              f"| {papers[doi]['authors'][0].split(',')[0][:15]:15} "
              f"| {papers[doi]['pubyear']} | {papers[doi]['pubmonth']:3}   "
              f"| {papers[doi]['journal'][:30]:30} | {papers[doi]['source']:9} "
              f"| {len(papers[doi]['citations']):4}       |")
    print(f"+{'-'*29}+{'-'*18}+{'-'*17}+{'-'*6}+{'-'*7}+{'-'*32}+{'-'*11}+{'-'*12}+")
    print()
    print(
        f"Missing papers: {[doi for doi in papers if papers[doi]['status'] == 'Missing']}")
    print()
    print(f"Total number of papers: {len(papers)}")
    fa = len([1 for i in papers if name in papers[i]['authors'][0]])
    print(f"Total number of first author papers: {fa}")
    tc = sum([len(papers[doi]['citations']) for doi in papers])
    print(f"Total number of citations: {tc}")


def make_publist(papers, caller):
    ''' Prepare mark down publication list to pdf
    '''
    with open("publications.md", 'w') as md_file:
        md_file.write("## Publications\n\n")
        md_file.write(str(len(papers))+" refereed papers (")
        md_file.write(str(sum([1 for doi in papers if caller in papers[doi]
                      ['authors'][0]]))+" as first author); more than ")
        md_file.write(
            str(math.floor(sum([len(papers[doi]['citations']) for doi in papers])/100)*100)+" citations (")
        md_file.write(
            "h-index of "+str(plots.hindex_calc(papers)[0][-1])+")\n\n")

        for idx, doi in enumerate(papers):
            md_file.write("("+str(idx+1)+") ")
            flag = 0

            for pos, fullname in enumerate(papers[doi]['authors']):
                if ',' in fullname:
                    surname = fullname.split(', ')[0]
                    nameparts = fullname.split(', ')[1:][0].split(' ')
                else:
                    surname = fullname.split(' ')[0]
                    nameparts = fullname.split(' ')[1:][0].split(' ')

                for entry, part in enumerate(nameparts):
                    nameparts[entry] = part[0]+'.'

                name = (' ').join([surname]+nameparts)

                if pos == len(papers[doi]['authors'])-1:
                    md_file.write(" and ")
                if caller in name:
                    md_file.write("__"+name+"__")
                    flag = 1
                elif pos > 10:
                    if flag == 0:
                        md_file.write("**et al.**")
                    else:
                        md_file.write("et al.")
                    break
                else:
                    md_file.write(name)
                if pos != len(papers[doi]['authors'])-1 and len(papers[doi]['authors']) > 2:
                    md_file.write(", ")

            md_file.write("<BR>")
            md_file.write(papers[doi]['title']+"<BR>")

            try:
                md_file.write(papers[doi]['journal'] + ", "+str(papers[doi]['volume']) +
                              ", "+str(papers[doi]['pages'])+", ")
            except:
                print(papers[doi]['journal'])
                pass

            month = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May',
                     'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            md_file.write(month[int(papers[doi]['pubmonth'])] +
                          " "+str(int(papers[doi]['pubyear'])))
            if len(papers[doi]['citations']) > 0:
                md_file.write(
                    " ("+str(len(papers[doi]['citations']))+" citations)")
            md_file.write("<BR>")
            md_file.write("\n\n")
