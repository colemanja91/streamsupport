from django.conf import settings

from asgiref.sync import sync_to_async
from aiohttp import ClientSession
from datetime import datetime, timedelta
from spnkr import AzureApp, HaloInfiniteClient, authenticate_player, refresh_player_tokens

# Wrapper for the SPNKr package: https://acurtis166.github.io/SPNKr/
# Most of this package is designed to work via async, so we abstract
# it's functionality to background jobs then analyze the offline data.

class RefreshTokenMissingException(Exception):
    pass

class SpnkrService:
  def __init__(self, xbox_user):
    self.xbox_user = xbox_user
    self.servicerecord = xbox_user.servicerecord
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
    if self.xbox_user.tokens_refreshed_at is not None:
      if self.xbox_user.tokens_refreshed_at > (datetime.now() - timedelta(hours=3, minutes=50)):
        return True
    
    async with ClientSession() as session:
      player = await refresh_player_tokens(session, self.app, self.xbox_user.refresh_token)
    
    self.xbox_user.spartan_token = player.spartan_token.token
    self.xbox_user.clearance_id = player.clearance_token.token
    await self.xbox_user.asave()

    return True

  async def refresh_service_record(self) -> None:
    await self.refresh_tokens()

    async with ClientSession() as session:
      client = HaloInfiniteClient(
        session=session,
        spartan_token=self.xbox_user.spartan_token,
        clearance_token=self.xbox_user.clearance_id
      )

      response = await client.stats.get_service_record(self.xbox_user.xuid)
      parsed = await response.parse()
      self.servicerecord.wins=parsed.wins
      self.servicerecord.losses=parsed.losses
      self.servicerecord.ties=parsed.ties
      self.servicerecord.matches_completed=parsed.matches_completed
      self.servicerecord.time_played=parsed.time_played
      await self.servicerecord.asave()
