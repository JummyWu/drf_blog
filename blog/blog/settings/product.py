import os
from .base import *
from decouple import config


DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wu_blog',
        'USER': 'root',
        'PASSWORD': 'Canbee2018!',
        'HOST': '111.230.25.51',
        "PORT": '3306',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/4',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        }
    }
}

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {  # 定义限流速率，支持秒、分、时、天的限制
        'anon': '150/day',
        'user': '250/day'
    },
    'DEFAULT_VERSION': "v1",  # 默认版本
    'ALLOWED_VERSIONS': ['v1', 'v2'],  # 可选版本
    # # 限制访问类
    # 'DEFAULT_THROTTLE_CLASSES': ('rest_framework.throttling.UserRateThrottle',
    #                              'rest_framework.throttling.AnonRateThrottle'),
    # 版本获取方式 分url 带参数等
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    # 验证用户类  使用django jwt
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}
REST_FRAMEWORK_EXTENSIONS = {
    # 缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60,
    # 缓存存储
    'DEFAULT_USE_CACHE': 'default',
}
WECHAT_APP_ID = 'wxc4d8c0dc77ee196e'
WECHAT_APPSECRET = '92599220115451d6602e9573d8c0418d'
WECHAT_TOKEN = 'jummywu'
