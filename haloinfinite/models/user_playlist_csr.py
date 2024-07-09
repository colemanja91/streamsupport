from django.db import models
from .playlist_asset import PlaylistAsset
from .xbox_user import XBoxUser

class UserPlaylistCSR(models.Model):
  xbox_user = models.ForeignKey(XBoxUser, on_delete=models.CASCADE)
  playlist_asset = models.ForeignKey(PlaylistAsset, on_delete=models.CASCADE, null=True)
  value = models.IntegerField(default=0)
  tier = models.CharField(default=None, null=True)
  tier_start = models.IntegerField(default=0)
  sub_tier = models.CharField(default=None, null=True)
  next_tier = models.CharField(default=None, null=True)
  next_tier_start = models.IntegerField(default=0)
  next_sub_tier = models.CharField(default=None, null=True)
