# April 27, 2010 loadCities.py
#reads in all sites and url from craigslist

from django.core.management.base import BaseCommand
from craigslist.models import *

class Command(BaseCommand):

    def handle(self, *test_labels, **options):
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
                            newSite = cl_Site(name=tr[1].td.a.contents[0], url=tr[1].td.a['href'])
                            newSite.save()
                            print tr[1].td.a['href']
                            tr[1].td.a = tr[1].td.a.nextSibling
                        tr[1].td = tr[1].td.nextSibling
                        while tr[1].td.a:
                            newSite = cl_Site(name=tr[1].td.a.contents[0], url=tr[1].td.a['href'])
                            newSite.save()
                            print tr[1].td.a['href']
                            tr[1].td.a = tr[1].td.a.nextSibling
                except:
                    while tr[1].td.a:
                            try:
                                print tr[1].td.a['href']
                                newSite = cl_Site(name=tr[1].td.a.contents[0], url=tr[1].td.a['href'])
                                newSite.save()
                            except:
                                print tr[1].td.a.contents[0]
                            try:
                                tr[1].td.a = tr[1].td.a.nextSibling.nextSibling  
                            except:
                                tr[1].td.a = tr[1].td.a.nextSibling             
        
            tr[0].td = tr[0].td.nextSibling
    