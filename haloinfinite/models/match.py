from django.db import models
from .playlist_asset import PlaylistAsset
from .xbox_user import XBoxUser

class Match(models.Model):
  xbox_user = models.ForeignKey(XBoxUser, on_delete=models.CASCADE)
  external_id = models.UUIDField(primary_key=True)
  outcome = models.CharField()
  rank = models.IntegerField(null=True)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  lifecycle_mode = models.CharField()
  game_variant = models.CharField()
  level_external_id = models.UUIDField()
  playlist_asset = models.ForeignKey(PlaylistAsset, on_delete=models.CASCADE, null=True)
  season_external_id = models.CharField(null=True)
  rounds_won = models.IntegerField(default=0)
  rounds_lost = models.IntegerField(default=0)
  rounds_tied = models.IntegerField(default=0)
  kills = models.IntegerField(default=0)
  deaths = models.IntegerField(default=0)
  assists = models.IntegerField(default=0)
  callout_assists = models.IntegerField(default=0)
  score = models.IntegerField(default=0)
  max_killing_spree = models.IntegerField(default=0)
  accuracy = models.FloatField(default=0)
  pre_match_csr = models.IntegerField(default=0)
  post_match_csr = models.IntegerField(default=0)
  stats_retrieved = models.BooleanField(default=False)
