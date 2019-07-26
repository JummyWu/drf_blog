"""
WSGI config for blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


profile = os.environ.get('BLOG_PROFILE', 'development')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings.%s' % profile)

application = get_wsgi_application()
