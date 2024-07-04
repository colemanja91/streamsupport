from django.db import models

class PlaylistAsset(models.Model):
  class Meta():
    models.UniqueConstraint(fields=['external_id', 'version_external_id'], name='unique_playlist_versions')

  external_id = models.UUIDField()
  version_external_id = models.UUIDField()
  public_name = models.CharField(null=True)
  description = models.CharField(null=True)
  info_retrieved = models.BooleanField(default=False)
