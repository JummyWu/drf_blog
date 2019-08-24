"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from django.views.decorators.csrf import csrf_exempt

from aricle.views import CategoryView, TagView, AricleView, HomeImgView
from user.views import ProfileView
from comment.views import CommentViewSet
from likes.views import LikeViewSet
from utils import ImageUploadView


routers = routers.DefaultRouter()
routers.register(r'category', CategoryView, base_name='category')
routers.register(r'tag', TagView, base_name='tag')
routers.register(r'aricle', AricleView, base_name='aricle')
routers.register(r'user', ProfileView, base_name='user')
routers.register(r'comment', CommentViewSet, base_name='comment')
routers.register(r'like', LikeViewSet, base_name='like')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^simditor/', include('simditor.urls')),
    url(r'^simditor/upload', csrf_exempt(ImageUploadView.as_view())),
    url(r'^(?P<version>(v1|v2))/', include(routers.urls)),  # 版本控制
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^users/', include('user.urls')),  # GIt登陆接口
    url(r'^(?P<version>(v1|v2))/login/', obtain_jwt_token),
    url(r'^home_img/$', HomeImgView.as_view()),
    url(r'^wx/', include('wechat.urls', namespace='wechat')),
    url(r'^', TemplateView.as_view(template_name="index.html"), name="index"),
]
