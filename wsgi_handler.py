import os, sys
#sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append('/home/balaa/webapps/glean')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

