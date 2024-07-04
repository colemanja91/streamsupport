from django.db import models

class XBoxUser(models.Model):
  xuid = models.CharField()
  gamertag = models.CharField(max_length=32)
  spartan_token = models.CharField(null=True)
  clearance_id = models.CharField(null=True)
  tokens_refreshed_at = models.DateTimeField(null=True)
  refresh_token = models.CharField(null=True)
