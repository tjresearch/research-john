import logging
from typing import List

import requests
from social_django.utils import load_strategy

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models

logger = logging.getLogger(__name__)

# Create your models here.


class UserManager(DjangoUserManager):
    pass


class User(AbstractBaseUser):
    objects = UserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []

    id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=32)
    email = models.EmailField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):  # pylint: disable=unused-argument
        return self.is_superuser

    def has_module_perms(self, app_label):  # pylint: disable=unused-argument
        return self.is_superuser

    def api_request(self, url, params=None, refresh=True):
        if params is None:
            params = {}
        social = self.get_social_auth()
        params.update({"format": "json"})
        params.update({"access_token": social.access_token})
        res = requests.get("https://ion.tjhsst.edu/api/{}".format(url), params=params)
        if res.status_code == 401:
            if refresh:
                try:
                    self.get_social_auth().refresh_token(load_strategy())
                except BaseException as ex:  # pylint: disable=broad-except
                    logger.exception(str(ex))
                return self.api_request(url, params, False)
            else:
                logger.error("Ion API Request Failure: %s %s", res.status_code, res.json())
        return res.json()

    def get_social_auth(self):
        return self.social_auth.get(provider="ion")

    def __str__(self):
        return self.username

    def __repr__(self):
        return "<User: {} ({})>".format(self.username, self.id)
