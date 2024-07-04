from annoying.fields import AutoOneToOneField
from django.db import models
from .xbox_user import XBoxUser

class ServiceRecord(models.Model):
  time_played = models.DurationField(null=True)
  matches_completed = models.IntegerField(default=0)
  wins = models.IntegerField(default=0)
  losses = models.IntegerField(default=0)
  ties = models.IntegerField(default=0)
  xbox_user = AutoOneToOneField(
    XBoxUser,
    on_delete=models.CASCADE,
    primary_key=True
  )
