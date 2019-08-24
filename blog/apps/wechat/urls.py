
from django.conf.urls import url
from .views import weixin_main

app_name = 'wechat'

urlpatterns = [
    url(r'^$', weixin_main, name='weixin_main'),
    ]
