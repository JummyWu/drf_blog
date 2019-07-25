from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from user.models import Profile

# Create your models here.

class LikeCount(models.Model):
    """对象点赞总数表"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.IntegerField(verbose_name='被点赞对象id')
    content_object = GenericForeignKey('content_type', 'object_id')
    likes_num = models.IntegerField(default=0, verbose_name='点赞数量')

    class Meta:
        verbose_name = '点赞总数'
        verbose_name_plural = '点赞总数'


class LikeRecord(models.Model):
    """用户点赞记录表"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='被点赞对象id')
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,
                             verbose_name='点赞用户')
    liked_time = models.DateField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        verbose_name = '用户点赞记录'
        verbose_name_plural = '用户点赞记录'
