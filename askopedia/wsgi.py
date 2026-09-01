"""
WSGI config for askopedia project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askopedia.settings')

application = get_wsgi_application()