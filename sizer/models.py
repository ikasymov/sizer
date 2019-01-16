# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model

from inobi import utils

User = get_user_model()

# Create your models here.


class Photo(models.Model):
    user = models.ForeignKey(User, related_name='photos', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(max_length=500, upload_to=utils.users_image_path)

