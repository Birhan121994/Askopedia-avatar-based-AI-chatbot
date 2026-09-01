"""
ASGI config for askopedia project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'askopedia.settings')

application = get_asgi_application()