from django.contrib import admin

from .models import PostComment


# class PostCommentAdmin(object):
#     list_display = ['content', 'time', 'user', 'object_id', 'parent',
#                     'reply_to', 'root']
#     list_filter = ['content', 'time', 'user', 'object_id', 'parent', 'reply_to',
#                    'root']


admin.site.register(PostComment)