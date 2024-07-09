from django.core.management.base import BaseCommand, CommandError
from haloinfinite.models import PlaylistAsset, XBoxUser
from haloinfinite.services import RefreshPlaylistCSR

class Command(BaseCommand):
  help = "Refresh a user's playlist CSR"

  def add_arguments(self, parser):
      parser.add_argument("xbox_user_id", type=int)
      parser.add_argument("playlist_asset_id", type=int)

  def handle(self, *args, **options):
    xbox_user_id = options["xbox_user_id"]
    playlist_asset_id = options["playlist_asset_id"]
    try:
      xbox_user = XBoxUser.objects.get(pk=xbox_user_id)
      playlist_asset = PlaylistAsset.objects.get(pk=playlist_asset_id)
    except XBoxUser.DoesNotExist:
      raise CommandError(f"XBoxUser {xbox_user_id} does not exist")
    except PlaylistAsset.DoesNotExist:
      raise CommandError(f"PlaylistAsset {playlist_asset_id} does not exist")
    
    RefreshPlaylistCSR(xbox_user, playlist_asset).run()
