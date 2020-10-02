"""
WSGI config for samriddhi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

sys.path.append('d:/GauravD/Samriddhi')
sys.path.append('d:/GauravD/Samriddhi/samriddhi')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samriddhi.settings')

application = get_wsgi_application()
