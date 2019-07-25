import markdown

from django.db import models
from django.db.models import F
from django.contrib.contenttypes.fields import GenericRelation

from user.models import Profile as User
from likes.models import LikeRecord, LikeCount

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '分类'


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '标签'


class Aricle(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    desc = models.CharField(max_length=100, blank=True, verbose_name='摘要')
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField('Tag', related_name='posts', verbose_name='标签')
    content = models.TextField(verbose_name='内容', help_text='目前支持markdown')
    is_markdown = models.BooleanField(verbose_name='使用markdown', default=True)
    html = models.TextField(verbose_name='渲染后的格式', default='')
    img = models.ImageField(upload_to='article/img', blank=True, null=True, verbose_name='封面图')
    owner = models.ForeignKey(User, verbose_name='作者', on_delete=models.DO_NOTHING)
    pv = models.PositiveIntegerField(default=0, verbose_name='pv')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    like_record = GenericRelation(LikeRecord)
    Like_count = GenericRelation(LikeCount)

    def __str__(self):
        return self.title

    def increse_pv(self):
        return type(self).objects.filter(id=self.id).update(pv=F('pv') + 1)

    def save(self, *args, **kwargs):
        config = {
            'codehilite': {
                'use_pygments': False,
                'css_class': 'prettyprint linenums code-padding',
            }
        }
        self.html = markdown.markdown(
            self.content,
            extensions=["codehilite", "fenced_code", "nl2br"],
            extension_configs=config
        )
        return super(Aricle, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = verbose_name = '文章'
        ordering = ['-id']
