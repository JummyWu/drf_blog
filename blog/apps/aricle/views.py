from django.views import View
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.core.cache import cache
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin

from .models import Category, Tag, Aricle
from .serializer import CategorySerializer, TagSerializer, AricleSerializer, ArtcleListSerializer
from .filters import CategoryFilter, TagFilter
from utils import img_data
from likes.models import LikeRecord


# Create your views here.


def cache_it(func):
    def wrapper(self, *args, **kwargs):
        key = repr((func.__name__, args, kwargs))
        result = cache.get(key)
        if result:
            return result
        result = func(self, *args, **kwargs)
        cache.set(key, result, 60 * 5)
        return result
    return wrapper


class AriclePagination(PageNumberPagination):
    page_size = 10


class CategoryView(ListModelMixin, RetrieveModelMixin, GenericViewSet, ListCacheResponseMixin):
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


class TagView(viewsets.ModelViewSet, ListModelMixin, ListCacheResponseMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class AricleView(ListModelMixin, RetrieveModelMixin, GenericViewSet, ListCacheResponseMixin):
    queryset = Aricle.objects.all()
    serializer_class = AricleSerializer
    pagination_class = AriclePagination
    # 设置三大常用过滤器DjangoFilterBackend
    filter_backends = (CategoryFilter, TagFilter,)
    filter_fields = ['title', ]
    content_model = None

    def get_queryset(self):
        item = self.request.query_params
        type_str = item.get('type')
        if type_str == 'search':
            search = item.get('search', None)
            if not search:
                return self.queryset
            return Aricle.objects.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return self.queryset

    @cache_response(60 * 60, cache='default')
    def list(self, request, *args, **kwargs):
        try:
            self.serializer_class = ArtcleListSerializer
            ret = super().list(request, *args, **kwargs)
            res_data = {}
            res_data['state'] = 200
            res_data['result'] = ret.data
            ret.data = res_data
            return ret
        except Exception:
            raise exceptions.NotFound("获取列表失败")

    @cache_response(60 * 60)
    def retrieve(self, request, *args, **kwargs):
        """is_Like判断是否点赞"""
        try:
            token = request.auth
            path = self.request.path
            pv_key = 'pv:%s:%s' % (token, path)
            if not cache.get(pv_key):
                instance = self.get_object()
                instance.pv += 1
                instance.save()
                cache.set(pv_key, 1, 60)
            self.serializer_class = AricleSerializer
            res = super().retrieve(request, *args, **kwargs)
            if isinstance(request.user, AnonymousUser):
                res.data['is_like'] = False  # 未登录默认没有点赞
            elif LikeRecord.objects.filter(content_type=self.content_model,
                                           object_id=kwargs['pk'],
                                           user=request.user):
                res.data['is_like'] = True
            else:
                res.data['is_like'] = False
            return res
        except Exception:
            raise exceptions.NotFound("获取详情失败")

    def get_object(self):
        obj = super().get_object()
        self.content_model = ContentType.objects.get_for_model(obj)
        return obj


class HomeImgView(View):
    def get(self, request, *args, **kwargs):
        url = img_data()
        return JsonResponse({"url": url})
