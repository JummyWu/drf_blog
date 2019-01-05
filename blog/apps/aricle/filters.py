# coding: utf-8
__author__ = 'jummy'

from django_filters import rest_framework as filter
from .models import Aricle


class AricleFilter(filter.FilterSet):
    title_name = filter.CharFilter(title='title', lookup_expr='icontains')

    class Meta:
        model = Aricle
        fields = ['title_name']
