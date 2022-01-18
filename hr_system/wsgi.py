"""
WSGI config for hr_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os, sys

#sys.path.append('/home/k/kursokrf/hr/public_html')
#sys.path.append('/home/k/kursokrf/hr')
#sys.path.append('/home/k/kursokrf/.djangovenv/lib/python3.8/site-packages/')
#sys.path.remove('/usr/lib/python3.8/site-packages')
#os.environ["DJANGO_SETTINGS_MODULE"] = hr_system.settings


from django.core.wsgi import get_wsgi_application

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_system.settings')

application = get_wsgi_application()
