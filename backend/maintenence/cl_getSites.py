from BeautifulSoup import BeautifulSoup
import urllib

SITES_URL = 'http://www.craigslist.org/about/sites'

#Read craigslist sites page into a variable
data = urllib.URLopener().open(SITES_URL).read()
data = data.replace('\n', '')
data = data.replace('\t', '')

#Pass sites pages to BeautifulSoup parser
soup = BeautifulSoup(data)

tr = soup.findAll('tr')

while tr[0].td:
    if tr[0].td.b:
        print tr[0].td.b.contents[0]
        tr[1].td = tr[1].td.nextSibling
        try:
            if tr[0].td.attrs[0] == (u'colspan', u'2'):
                while tr[1].td.a:
                    print tr[1].td.a['href']
                    tr[1].td.a = tr[1].td.a.nextSibling
                tr[1].td = tr[1].td.nextSibling
                while tr[1].td.a:
                    print tr[1].td.a['href']
                    tr[1].td.a = tr[1].td.a.nextSibling
        except:
            while tr[1].td.a:
                    try:
                        print tr[1].td.a['href']
                    except:
                        print tr[1].td.a.contents[0]
                    try:
                        tr[1].td.a = tr[1].td.a.nextSibling.nextSibling  
                    except:
                        tr[1].td.a = tr[1].td.a.nextSibling             
        
    tr[0].td = tr[0].td.nextSibling
    