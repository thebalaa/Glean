# April 27, 2010 loadCategories.py
#reads in all categories and their url slugs

from django.core.management.base import BaseCommand
from craigslist.models import *

cl_GleanEngine = '/home/balaa/webapps/glean/manage.py cl_GleanEngine '
cl_GleanDaemon = '/home/balaa/webapps/glean/manage.py cl_GleanDaemon'
TMP_CRONTAB = '/home/balaa/webapps/tmp/glean/crontab'
class Command(BaseCommand):

    def handle(self, *test_labels, **options):
        try:
            queries = cl_GleanQuery.objects.filter(active=True)
        except:
            queries = []
        try:
            file = open(TMP_CRONTAB, 'wr')
        except:
            file = open(TMP_CRONTAB, 'w')
        from subprocess import Popen
        if queries:
            write_data = '* * * * * ' + cl_GleanDaemon +'\n'
            file.write(write_data)
            for query in queries:
                if query.execution_frequency:
                    write_data = '*/'+ str(query.execution_frequency) +' * * * * ' + cl_GleanEngine + str(query.pk)+'\n'
                else:
                    write_data = '* * * * * ' + cl_GleanEngine + str(query.pk)+'\n'
                file.write(write_data)
            file.close()
            Popen(["/usr/bin/crontab", "-u", "balaa", TMP_CRONTAB])
        else:
            write_data = '* * * * * ' + cl_GleanDaemon +'\n'
            file.write(write_data)
            file.close()
            Popen(["/usr/bin/crontab", "-u", "balaa", TMP_CRONTAB])