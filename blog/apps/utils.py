# coding: utf-8
__author__ = 'jummy'
import os
import random

from django.conf import settings
from django.contrib.contenttypes.models import ContentType


def get_ContentType(queryset):
    return ContentType.objects.get_for_model(queryset)


def img_list():
    with open(os.path.join(settings.BASE_DIR, 'img_url.txt'), 'r', encoding='utf-8') as img:
        data = list(set(img.read().split('\n')))

    def random_url():
        rad = random.Random()
        return data[rad.randint(0, len(data) - 1)]

    return random_url

img_data = img_list()
