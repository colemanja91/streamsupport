import asyncio

from haloinfinite.models import Match, PlaylistAsset
from .spnkr_service import SpnkrService

class RefreshMatches:
  def __init__(self, xbox_user):
    self.xbox_user = xbox_user
    self.spnkr = SpnkrService(self.xbox_user)
  
  def run(self):
    results = asyncio.run(self.spnkr.refresh_matches())

    for result in results:
      playlist_asset, _playlist_asset_created = PlaylistAsset.objects.get_or_create(
        external_id=result.match_info.playlist.asset_id,
        version_external_id=result.match_info.playlist.version_id
      )

      Match.objects.get_or_create(
        xbox_user=self.xbox_user,
        external_id=result.match_id,
        outcome=result.outcome.value,
        rank=result.rank,
        start_time=result.match_info.start_time,
        end_time=result.match_info.end_time,
        game_variant=result.match_info.game_variant_category.value,
        level_external_id=result.match_info.level_id,
        playlist_asset=playlist_asset,
        season_external_id=result.match_info.season_id
      )