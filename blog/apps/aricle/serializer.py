# coding: utf-8
__author__ = 'jummy'

from rest_framework import serializers

from .models import Category, Tag, Aricle
from utils import get_ContentType
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


class AricleSerializer(serializers.ModelSerializer):
    owner = ProfileSerializers()
    category = CategorySerializer()
    tags = TagSerializer(read_only=True, many=True)
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')

    class Meta:
        model = Aricle
        fields = '__all__'
