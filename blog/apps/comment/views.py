from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializer import CommentSerializer
from .models import PostComment
from aricle.serializer import content_type as article_contentType
from aricle.views import AriclePagination


# Create your views here.


class ResponseComment:
    """创建留言并返回前台所需要的数据"""
    def __init__(self, obj):
        self.obj = obj

    def get_dict(self):
        comment_dict = {}
        for filder in self.obj._meta.fields:
            column = filder.column
            if column == "user_id":
                img = str(getattr(self.obj, 'user', None).img)
                comment_dict['username'] = getattr(self.obj, 'user',
                                                   None).username
                comment_dict['user_img'] = img
            elif column == 'time':
                time = getattr(self.obj, column)
                comment_dict[column] = time.strftime('%Y-%m-%d %H:%M:%S')
                continue
            elif column == 'parent_id':
                continue
            elif column == 'reply_to_id' and getattr(self.obj, column,
                                                     None) is not None:
                comment_dict['reply_to'] = getattr(self.obj, 'reply_to',
                                                   None).username
            elif column == 'root_id':
                comment_dict['root'] = []
            comment_dict[column] = getattr(self.obj, column, None)
        comment_dict['is_like'] = False
        comment_dict['like_num'] = 0
        return comment_dict


class CommentViewSet(ListModelMixin, GenericViewSet):
    """
    留言功能视图：create list
    """
    queryset = PostComment.objects.exclude(root__isnull=False).order_by('-time')
    permission_classes = (IsAuthenticated,)  # 判断是否登陆
    serializer_class = CommentSerializer
    pagination_class = AriclePagination

    def get_queryset(self):
        """获取本篇文章的留言"""
        object_id = int(self.request.query_params.get('object_id')[0])
        queryset = PostComment.objects.exclude(root__isnull=False).filter(
            content_type=article_contentType, object_id=object_id).order_by(
            '-time')
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        response = ResponseComment(obj).get_dict()
        return Response(response)

    def get_permissions(self):
        if self.request.method.lower() == "get":
            self.permission_classes = ()
        return super().get_permissions()
