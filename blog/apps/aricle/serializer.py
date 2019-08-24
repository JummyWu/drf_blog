# coding: utf-8
__author__ = 'jummy'

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Category, Tag, Aricle
from utils import get_ContentType, img_data
from user.serializer import ProfileSerializers


content_type = get_ContentType(Aricle)


class CategorySerializer(serializers.ModelSerializer):
    owner = ProfileSerializers()
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    owner = ProfileSerializers()
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Tag
        fields = '__all__'


class LikeRecordSerializer(serializers.Serializer):
    """点赞记录  用于文章详情页点赞用户生成数据"""
    user = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_img = serializers.SerializerMethodField()
    user_git = serializers.SerializerMethodField()
    liked_time = serializers.SerializerMethodField()

    def get_user(self, queryset):
        return queryset['user']

    def get_user_name(self, queryset):
        return queryset['user__username']

    def get_user_img(self, queryset):
        return queryset['user__img']

    def get_liked_time(self, queryset):
        return queryset['liked_time']

    def get_user_git(self, queryset):
        return queryset['user__git_path']


class AricleSerializer(ModelSerializer):
    """文章详情"""
    category = CategorySerializer()
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    like_count = serializers.SerializerMethodField()
    like_record = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    def get_like_count(self, queryset):
        obj, created = queryset.Like_count.get_or_create(
            content_type=content_type,
            object_id=queryset.id)
        return obj.likes_num

    def get_like_record(self, queryset):
        obj = queryset.like_record.filter(
            content_type=content_type,
            object_id=queryset.id).values('user', 'user__username', 'user__img',
                                          'liked_time', 'user__git_path')
        return LikeRecordSerializer(obj, many=True).data

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_relate('owner')
        queryset = queryset.select_relate('category')
        queryset = queryset.prefetch_related('tags')
        return queryset

    class Meta:
        model = Aricle
        fields = ('id', 'html', 'title', 'add_time', 'category',
                        'like_count', 'like_record', 'pv', 'tags')


class ArtcleListSerializer(ModelSerializer):
    """文章列表"""
    category = CategorySerializer()
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    like_count = serializers.SerializerMethodField()    # 点赞数
    cover = serializers.SerializerMethodField()     # 封面图
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    def get_cover(self, queryset):
        return img_data()

    def get_like_count(self, queryset):
        obj, created = queryset.Like_count.get_or_create(
            content_type=content_type,
            object_id=queryset.id)
        return obj.likes_num

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.prefetch_related('tags')
        return queryset

    class Meta:
        model = Aricle
        fields = ('id', 'title', 'cover', 'add_time', 'category', 'like_count', 'pv', 'tags')

