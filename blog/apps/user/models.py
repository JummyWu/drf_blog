from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Profile(AbstractUser):
    """用户资料"""
    img = models.ImageField(upload_to='users', max_length=200, null=True,
                            blank=True, verbose_name='头像')
    github_id = models.PositiveIntegerField('Github_id', unique=True, null=True, blank=True)

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name_plural = verbose_name = '用户资料'
