# coding: utf-8
__author__ = 'jummy'
from rest_framework import serializers
from django.contrib.auth.models import AnonymousUser

from .models import PostComment
from aricle.serializer import content_type as article_contentType
from utils import get_ContentType
from likes.models import LikeCount, LikeRecord


content_type = get_ContentType(PostComment)


class SubCommentSerializer(serializers.ModelSerializer):
    """序列化子留言"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    username = serializers.SerializerMethodField()
    reply_to = serializers.SerializerMethodField()
    user_img = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField(read_only=True)
    like_num = serializers.SerializerMethodField(read_only=True)
    is_like = serializers.SerializerMethodField(read_only=True)
    git_path = serializers.SerializerMethodField(read_only=True)

    login_user = None

    def __new__(cls, *args, **kwargs):
        cls.login_user = kwargs['login_user']
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        kwargs.pop('login_user')
        return super().__init__(self, *args, **kwargs)

    def get_username(self, queryset):
        return queryset.user.username

    def get_reply_to(self, queryset):
        return queryset.reply_to.username

    def get_user_img(self, queryset):
        return str(queryset.user.img)

    def get_user_id(self, queryset):
        return str(queryset.user.pk)

    def get_git_path(self, queryset):
        return str(queryset.user.git_path)

    def get_like_num(self, queryset):
        obj = LikeCount.objects.filter(content_type=content_type,
                                       object_id=queryset.id).first()
        if (obj):
            return obj.likes_num
        return 0

    def get_is_like(self, queryset):
        if isinstance(self.context['request'].user, AnonymousUser):
            return False
        obj = LikeRecord.objects.filter(content_type=content_type, object_id=queryset.id, user=self.context['request'].user.id)
        if obj:
            return True
        else:
            return False

    class Meta:
        model = PostComment
        fields = ['id', 'content', 'time', 'user_id', 'parent_id',
                  'reply_to_id',
                  'root_id', 'username', 'reply_to', 'user_img', 'like_num', 'is_like', 'user', 'git_path']


class CommentSerializer(serializers.Serializer):
    """父留言"""
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    object_id = serializers.IntegerField()
    parent_id = serializers.IntegerField()
    reply_to_id = serializers.IntegerField()
    root_id = serializers.IntegerField()
    time = serializers.DateTimeField(read_only=True,
                                     format='%Y-%m-%d %H:%M:%S')
    root = serializers.SerializerMethodField()
    user_img = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.SerializerMethodField(read_only=True)
    like_num = serializers.SerializerMethodField(read_only=True)
    is_like = serializers.SerializerMethodField(read_only=True)
    git_path = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data):
        comment = PostComment()
        comment.content_type = article_contentType
        comment.object_id = validated_data['object_id']
        comment.user = validated_data['user']
        comment.content = validated_data['content']
        comment.parent_id = validated_data['parent_id'] if validated_data[
                                                               'parent_id'] != \
                                                           0 else None
        comment.reply_to_id = validated_data['reply_to_id'] if validated_data[
                                                                   'reply_to_id'] != 0 else None
        comment.root_id = validated_data['root_id'] if validated_data[
                                                           'root_id'] != 0 else None
        comment.save()
        return comment

    def get_root(self, queryset):
        queryset = queryset.root_comment.all()
        data = SubCommentSerializer(queryset, login_user=self.context['request'].user, many=True).data
        return data

    def get_user_img(self, queryset):
        return str(queryset.user.img)

    def get_username(self, queryset):
        return str(queryset.user.username)

    def get_user_id(self, queryset):
        return queryset.user_id

    def get_git_path(self, queryset):
        return str(queryset.user.git_path)

    def get_like_num(self, queryset):
        obj = LikeCount.objects.filter(content_type=content_type,
                                       object_id=queryset.id).first()
        if (obj):
            return obj.likes_num
        return 0

    def get_is_like(self, queryset):
        if isinstance(self.context['request'].user, AnonymousUser):
            return False
        obj = LikeRecord.objects.filter(content_type=content_type, object_id=queryset.id, user=self.context['request'].user.id)
        if obj:
            return True
        else:
            return False
