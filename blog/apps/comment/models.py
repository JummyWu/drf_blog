from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from user.models import Profile
from likes.models import LikeCount


# Create your models here.


class PostComment(models.Model):
    content = models.CharField(max_length=500, verbose_name='评论')
    time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    user = models.ForeignKey(Profile, related_name='comments',
                             on_delete=models.CASCADE, verbose_name='评论用户')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     verbose_name='评论类型对象')
    object_id = models.IntegerField(verbose_name='对象id')
    content_object = GenericForeignKey('content_type', 'object_id')
    parent = models.ForeignKey('self', related_name='parent_comment', null=True,
                               blank=True, on_delete=models.CASCADE,
                               default=None, verbose_name='上级留言')
    reply_to = models.ForeignKey(Profile, related_name='reply', null=True,
                                 on_delete=models.CASCADE, default=None,
                                 verbose_name='被回复用户对象')
    root = models.ForeignKey('self', related_name='root_comment', null=True,
                             on_delete=models.CASCADE, default=None,
                             verbose_name='顶级留言')
    like_count = GenericRelation(LikeCount)

    # root 用与顶级留言反查下级留言

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['time']
        verbose_name = '评论'
        verbose_name_plural = '评论'
