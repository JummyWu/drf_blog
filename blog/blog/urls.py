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
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from aricle.views import CategoryView, TagView, AricleView
from user.views import ProfileView

routers = routers.DefaultRouter()
routers.register(r'category', CategoryView, base_name='category')
routers.register(r'tag', TagView, base_name='tag')
routers.register(r'aricle', AricleView, base_name='aricle')
routers.register(r'user', ProfileView, base_name='user')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(routers.urls)),
    url('^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
