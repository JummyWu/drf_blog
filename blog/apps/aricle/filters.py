# coding: utf-8
__author__ = 'jummy'

from django_filters import rest_framework as filter
from django_filters import exceptions

from .models import Aricle


class AricleFilter(filter.FilterSet):
    title_name = filter.CharFilter(title='title', lookup_expr='icontains')

    class Meta:
        model = Aricle
        fields = ['title_name']


class CategoryFilter:
    def filter_queryset(self, request, queryset, view):
        item = request.query_params
        try:
            if 'category' in item:
                category_id = int(item.get('category'))
                queryset = list(filter(lambda x: x.category_id == category_id, queryset))
        except Exception as e:
            raise exceptions.NotFound('查找的分类不存在')
        return queryset
