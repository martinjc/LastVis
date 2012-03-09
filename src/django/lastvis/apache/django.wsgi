import os
import sys

path = '/usr/local/www'
if path not in sys.path:
    sys.path.insert(0, path)

site_path = '/usr/local/www/foursqexp'
if site_path not in sys.path:
    sys.path.insert(0, site_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'lastvis.settings_production'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()