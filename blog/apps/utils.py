# coding: utf-8
__author__ = 'jummy'

from django.contrib.contenttypes.models import ContentType


def get_ContentType(queryset):
    return ContentType.objects.get_for_model(queryset)
