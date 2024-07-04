from django.db import models
from .xbox_user import XBoxUser

class ServiceRecord(models.Model):
  time_played = models.DurationField()
  wins = models.IntegerField()
  losses = models.IntegerField()
  ties = models.IntegerField()
  xbox_user = models.OneToOneField(
    XBoxUser,
    on_delete=models.CASCADE,
    primary_key=True
  )
