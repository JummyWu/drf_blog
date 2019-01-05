# coding: utf-8
__author__ = 'jummy'

from rest_framework import serializers
from .models import Profile


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        fields = ['id', 'last_login', 'username', 'first_name', 'last_name',
                  'email', 'img', 'github_id']
