# April 27, 2010 loadCategories.py
#reads in all categories and their url slugs

from django.core.management.base import BaseCommand
from craigslist.models import *

class Command(BaseCommand):

    def handle(self, *test_labels, **options):
        from BeautifulSoup import BeautifulSoup
        import urllib

        SITES_URL = 'http://atlanta.craigslist.org/'

        #Read craigslist sites page into a variable
        data = urllib.URLopener().open(SITES_URL).read()
        data = data.replace('\n', '')
        data = data.replace('\t', '')

        #Pass sites pages to BeautifulSoup parser
        soup = BeautifulSoup(data)

        main_table = soup.find(attrs={'id':'main'})
        
        category = main_table.tr.nextSibling
        
        while category.td:
        
            while category.td.div.a:
                if category.td.div.h4.a:
                    print category.td.div.h4.a
                    newCat = cl_Category(name=category.td.div.h4.a.contents[0], slug=category.td.div.h4.a['href'])
                    newCat.save()
                    ul = category.td.div.ul
                    try:
                        while ul.li:
                            while ul.li:
                                print ul.li.a
                                newSubCat = cl_Category_subCat(name=ul.li.a.contents[0], slug=ul.li.a['href'], cl_Category=newCat)
                                newSubCat.save()
                                ul.li = ul.li.nextSibling
                            if ul.nextSibling:
                                ul = ul.nextSibling
                            else:
                                break
                            
                    except:
                        pass
                        
                if category.td.div.nextSibling:
                    category.td.div = category.td.div.nextSibling
                else:
                    break
            if category.td.nextSibling:
                category.td = category.td.nextSibling.nextSibling
            else:
                break    
    