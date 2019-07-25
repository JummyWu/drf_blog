from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import LikeRecord, LikeCount
from .serializers import LikesSerializers, CommentLikesSerializers, \
    content_type as comment_contentType, article_contentType


# Create your views here.


class LikeViewSet(GenericViewSet):
    """文章点赞"""
    queryset = LikeRecord.objects.all()
    serializer_class = LikesSerializers
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        data = {}
        data['status'] = 201
        data['name'] = obj.user.username
        data['id'] = obj.user.id
        data['time'] = obj.liked_time.strftime('%Y-%m-%d')
        img = obj.user.img
        data['img'] = str(img)
        return Response(data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {'id': self.request.user.id}
        return Response(data)

    def get_object(self):
        object_id = self.request.query_params['object_id'][0]
        obj = LikeRecord.objects.filter(object_id=object_id,
                                        content_type=article_contentType,
                                        user=self.request.user).first()
        return obj

    def perform_destroy(self, instance):
        obj = LikeCount.objects.filter(object_id=instance.object_id,
                                       content_type=instance.content_type).first()
        obj.likes_num -= 1
        obj.save()
        instance.delete()


class PostLikeVewSet(LikeViewSet):
    """留言点赞"""
    serializer_class = CommentLikesSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        data = {}
        data['status'] = 201
        data['like_num'] = obj.likes_num
        return Response(data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        data = {'status': 200}
        return Response(data)

    def get_object(self):
        object_id = self.request.query_params['object_id']
        obj = LikeRecord.objects.filter(object_id=object_id,
                                        content_type=comment_contentType,
                                        user=self.request.user).first()
        return obj

    def perform_destroy(self, instance):
        obj = LikeCount.objects.filter(object_id=instance.object_id,
                                       content_type=instance.content_type).first()
        obj.likes_num -= 1
        obj.save()
        instance.delete()
