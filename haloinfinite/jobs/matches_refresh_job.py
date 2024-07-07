from scheduler import job

from haloinfinite.models import XBoxUser
from haloinfinite.services import RefreshMatches, RefreshMatchStats, RefreshPlaylistInfo

def run():
  users = XBoxUser.objects.exclude(refresh_token__isnull=True)
  for user in users:
    RefreshMatches(user).run()
    RefreshMatchStats(user).run()
  
  # Only need to run this once
  RefreshPlaylistInfo(user).run()