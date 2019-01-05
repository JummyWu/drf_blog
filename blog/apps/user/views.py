import requests

from django.core.exceptions import PermissionDenied
from django.conf import settings
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .models import Profile
from .serializer import ProfileSerializers

# Create your views here.


class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers


class OauthView(APIView):
    access_token_url = None
    user_api = None
    client_id = None
    client_secret = None

    def get(self, *args, **kwargs):
        access_token = self.get_access_token()
        user_info = self.get_user_info(access_token)
        return self.authenticate(user_info)

    def get_access_token(self):
        url = self.access_token_url
        headers = {'Accept': 'application/json'}
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self.request.GET['code']
        }
        r = requests.post(url, data, headers=headers, timeout=5)
        result = r.json()
        if 'access_token' in result:
            return result['access_token']
        else:
            raise PermissionDenied

    def get_user_info(self, access_token):
        url = self.user_api + access_token
        r = requests.get(url, timeout=3)
        user_info = r.json()
        return user_info

    def get_success_url(self):
        if 'next' in self.request.session:
            return self.request.session.pop('next')
        else:
            return '/'


class GitHubOAuthView(OauthView):
    access_token_url = 'https://github.com/login/oauth/access_token'
    user_api = 'https://api.github.com/user?access_token='
    client_id = settings.GITHUB_CLIENT_ID
    client_secret = settings.GITHUB_CLIENT_SECRET

    def authenticate(self, user_info):
        user = Profile.objects.filter(github_id=user_info['id'])
        if not user:
            user = Profile.objects.create_user(user_info['login'], user_info['email'])
            user.github_id = user_info['id']
            user.img = user_info['avatar_url']
            user.save()
        else:
            user = user[0]
            if user.username != user_info['login'] or \
                user.img.url != user_info['avatar_url']:
                user.username = user_info['login']
                user.img = user_info['avatar_url']
                user.save()
        re_dict = {}
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.username
        re_dict['id'] = user.pk
        return Response(re_dict)
