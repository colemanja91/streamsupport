import asyncio

from haloinfinite.models import UserPlaylistCSR
from .spnkr_service import SpnkrService

from spnkr.models.refdata import SkillResultCode

class RefreshPlaylistCSR:
  def __init__(self, xbox_user, playlist_asset):
    self.xbox_user = xbox_user
    self.playlist_asset = playlist_asset
    self.spnkr = SpnkrService(self.xbox_user)
  
  def run(self):
    response = asyncio.run(self.spnkr.get_playlist_csr(self.playlist_asset.external_id))

    if response.value[0] and response.value[0].result_code == SkillResultCode.SUCCESS:
      current = response.value[0].result.current

      upc, _ = UserPlaylistCSR.objects.update_or_create(
        xbox_user=self.xbox_user, 
        playlist_asset=self.playlist_asset
      )

      upc.value=current.value
      upc.tier=current.tier.value
      upc.tier_start=current.tier_start
      upc.sub_tier=current.sub_tier.to_int()
      upc.next_tier=current.next_tier.value
      upc.next_tier_start=current.next_tier_start
      upc.next_sub_tier=current.next_sub_tier.value
      upc.save()
