"""
WSGI config for ExpenseTracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Add the directory containing the ExpenseTracker module to the Python path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ExpenseTracker.deployment" if 'WEBSITE_HOSTNAME' in os.environ else "ExpenseTracker.settings")
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', 'true')
sys.path.append('ExpenseTracker/')

# settings_module = 'ExpenseTracker.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'ExpenseTracker.settings'

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
