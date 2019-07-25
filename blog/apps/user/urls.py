# coding: utf-8
__author__ = 'jummy'

from django.conf.urls import url
from .views import GitHubOAuthView


urlpatterns = [
    url('^git/oauth/$', GitHubOAuthView.as_view(), name='github'),
]