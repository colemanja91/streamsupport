from datetime import timedelta
from django.db import models
from django.db.models import DurationField, ExpressionWrapper, F
from .playlist_asset import PlaylistAsset
from .xbox_user import XBoxUser

class MatchQuerySet(models.QuerySet):
  def ranked_slayer(self):
    return self.filter(playlist_asset__public_name='Ranked Slayer')
  
  def not_ended_early(self):
    expression = F('end_time') - F('start_time')
    wrapped = ExpressionWrapper(expression, DurationField())
    delta = timedelta(minutes=3)
    return self.annotate(match_duration=wrapped)\
      .exclude(
        outcome='1',
        score=0,
        match_duration__lte=delta
      )

class MatchManager(models.Manager):
  def get_queryset(self):
    return MatchQuerySet(self.model, using=self._db)
  
  def ranked_slayer(self):
    return self.get_queryset().ranked_slayer()
  
  def not_ended_early(self):
    return self.get_queryset().not_ended_early()

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

  objects = MatchManager()
