from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend


from .models import Category, Tag, Aricle
from .serializer import CategorySerializer, TagSerializer, AricleSerializer
from .filters import CategoryFilter
# Create your views here.


class AriclePagination(PageNumberPagination):
    page_size = 12
    # 向后台要多少条数据
    page_size_query_param = 'page_size'
    # 定制多少页数据
    page_query_param = 'page'
    max_page_size = 100


class CategoryView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        qs = super(CategoryView, self).get_queryset()
        if self.kwargs.get('pk'):
            cate_id = self.kwargs.get('pk')
            qs = qs.filter(id=cate_id)
            return qs
        else:
            return qs


class TagView(viewsets.ModelViewSet, ListModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AricleView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Aricle.objects.all()
    serializer_class = AricleSerializer
    pagination_class = AriclePagination
    # 设置三大常用过滤器DjangoFilterBackend
    filter_backends = (CategoryFilter, )
    filter_fields = ['title', ]
