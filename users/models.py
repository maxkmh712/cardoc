from django.db import models

from core.models import TimeStamp

class User(TimeStamp):
  login_id = models.CharField(max_length=100, unique=True)
  password = models.CharField(max_length=200)
  name     = models.CharField(max_length=50, null=True)

  class Meta:
    db_table = 'users'