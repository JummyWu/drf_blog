from django.contrib import admin

from .models import LikeCount, LikeRecord
# Register your models here.


admin.site.register(LikeCount)
admin.site.register(LikeRecord)