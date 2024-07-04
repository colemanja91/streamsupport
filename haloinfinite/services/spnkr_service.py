from django.conf import settings

from asgiref.sync import sync_to_async
from aiohttp import ClientSession
from datetime import datetime, timedelta
from spnkr import AzureApp, authenticate_player, refresh_player_tokens

# https://acurtis166.github.io/SPNKr/

class RefreshTokenMissingException(Exception):
    pass

class SpnkrService:
  def __init__(self, xbox_user):
    self.xbox_user = xbox_user
    self.app = AzureApp(settings.MSAL_CLIENT_ID, settings.MSAL_CLIENT_SECRET, settings.MSAL_REDIRECT_URI)
  
  # For now only use this from commands
  # Eventually add callback processing functionality
  async def get_refresh_token(self):
    async with ClientSession() as session:
      refresh_token = await authenticate_player(session, self.app)
    
    self.xbox_user.refresh_token = refresh_token
    await self.xbox_user.asave()

  async def refresh_tokens(self) -> None:
    if self.xbox_user.refresh_token is None:
      raise RefreshTokenMissingException(f"XBoxUser {self.xbox_user.id} does not have a refresh token.")
    
    # Spartan Tokens are valid for four hours
    if self.xbox_user.tokens_refreshed_at > (datetime.now() - timedelta(hours=3, minutes=50)):
      return True
    
    async with ClientSession() as session:
      player = await refresh_player_tokens(session, self.app, self.xbox_user.refresh_token)
    
    self.xbox_user.spartan_token = player.spartan_token.token
    self.xbox_user.clearance_id = player.clearance_token.token
    await self.xbox_user.asave()

    return True