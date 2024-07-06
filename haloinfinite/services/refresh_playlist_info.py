import asyncio

from haloinfinite.models import PlaylistAsset
from .spnkr_service import SpnkrService

class RefreshPlaylistInfo:
  def __init__(self, xbox_user):
    self.xbox_user = xbox_user
    self.spnkr = SpnkrService(self.xbox_user)
  
  def run(self):
    assets = PlaylistAsset.objects.all()

    for asset in assets:
      print(f"Fetching info for asset {asset.external_id} version {asset.version_external_id}")
      response = asyncio.run(self.spnkr.get_playlist(asset.external_id, asset.version_external_id))

      asset.public_name = response.public_name
      asset.description = response.description
      asset.save()
      print("Fetched!")
