# April 27, 2010 loadCategories.py
#reads in all categories and their url slugs

from django.core.management.base import BaseCommand
from craigslist.models import *
from craigslist.util import GleanCraig
import sys

cl_GleanEngine = '/home/balaa/webapps/glean/manage.py cl_GleanEngine '
cl_GleanDaemon = '/home/balaa/webapps/glean/manage.py cl_GleanDaemon'
TMP_CRONTAB = '/home/balaa/webapps/tmp/glean/crontab'
class Command(BaseCommand):

    def handle(self, *test_labels, **options):
        cl_GleanQueryId = sys.argv[2]
        query = cl_GleanQuery.objects.get(pk=cl_GleanQueryId)
        cl_GleanQueries = GleanCraig(query)
        cl_GleanQueries.glean()
                 
