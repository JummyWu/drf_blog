# coding: utf-8
from rest_framework import serializers
import django.utils.timezone as timezone
from django.contrib.contenttypes.models import ContentType

from .models import LikeRecord, LikeCount
from aricle.serializer import content_type as article_contentType
from comment.models import PostComment


content_type = ContentType.objects.get_for_model(PostComment)


class LikesSerializers(serializers.Serializer):
    """文章点赞"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    object_id = serializers.IntegerField()

    def create(self, validated_data):
        user = validated_data['user']
        obj_id = validated_data['object_id']
        like, created = LikeRecord.objects.get_or_create(
            content_type=article_contentType,
            object_id=obj_id,
            user=user,
        )
        like.liked_time = timezone.now()
        like.save()
        self.Like_count(article_contentType, obj_id)
        return like

    def Like_count(self, model, obj_id):
        count, created = LikeCount.objects.get_or_create(
            content_type=model,
            object_id=obj_id)
        count.likes_num += 1
        count.save()


class CommentLikesSerializers(LikesSerializers):
    """留言点赞"""
    def create(self, validated_data):
        user = validated_data['user']
        obj_id = validated_data['object_id']
        like, created = LikeRecord.objects.get_or_create(
            content_type=content_type,
            object_id=obj_id,
            user=user,
        )
        like.liked_time = timezone.now()
        like.save()
        count = self.Like_count(content_type, obj_id)
        return count

    def Like_count(self, model, obj_id):
        count, created = LikeCount.objects.get_or_create(
            content_type=model,
            object_id=obj_id)
        count.likes_num += 1
        count.save()
        return count
