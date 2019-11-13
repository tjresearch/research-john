from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Network(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
