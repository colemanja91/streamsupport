from haloinfinite.models import PlaylistAsset, XBoxUser
from haloinfinite.services import RefreshMatches, RefreshMatchStats, RefreshPlaylistCSR, RefreshPlaylistInfo, RefreshServiceRecord

def run():
  ranked_playlists = PlaylistAsset.objects.ranked_playlists()
  users = XBoxUser.objects.exclude(refresh_token__isnull=True)
  for user in users:
    RefreshServiceRecord(user).run()
    RefreshMatches(user).run()
    RefreshMatchStats(user).run()

    for ranked_playlist in ranked_playlists:
      RefreshPlaylistCSR(user, ranked_playlist)
  
  # Only need to run this once
  RefreshPlaylistInfo(users.first()).run()
