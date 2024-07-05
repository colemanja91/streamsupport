from django.conf import settings
from haloinfinite.models import Match, PlaylistAsset

from asgiref.sync import sync_to_async
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError
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
    
    return parsed
  
  async def refresh_matches(self) -> None:
    await self.refresh_tokens()

    async with ClientSession() as session:
      client = HaloInfiniteClient(
        session=session,
        spartan_token=self.xbox_user.spartan_token,
        clearance_token=self.xbox_user.clearance_id,
        requests_per_second=5
      )

      index = 0
      increment = 25
      has_more = True
      results = []

      while has_more:
        response = await client.stats.get_match_history(
          self.xbox_user.xuid,
          start=index,
          count=increment,
          match_type='matchmaking'
        )

        parsed = await response.parse()
        results.extend(parsed.results)

        print(f"Retrieved {len(results)} matches")

        index += increment
        if parsed.result_count < increment:
          has_more = False
      
      return results

  async def refresh_match_stats(self, matches) -> None:
    await self.refresh_tokens()

    async with ClientSession() as session:
      client = HaloInfiniteClient(
        session=session,
        spartan_token=self.xbox_user.spartan_token,
        clearance_token=self.xbox_user.clearance_id,
        requests_per_second=5
      )

      for match in matches:
        try:
          response = await client.stats.get_match_stats(match_id=match.external_id)
          parsed = await response.parse()
          player_stats = [player for player in parsed.players if (player.player_id == f"xuid({self.xbox_user.xuid})")][0]
          stats = player_stats.player_team_stats[0].stats.core_stats

          match.rounds_won = stats.rounds_won
          match.rounds_lost = stats.rounds_lost
          match.rounds_tied = stats.rounds_tied
          match.kills = stats.kills
          match.deaths = stats.deaths
          match.assists = stats.assists
          match.callout_assists = stats.callout_assists
          match.score = stats.score
          match.max_killing_spree = stats.max_killing_spree
          match.accuracy = stats.accuracy

          print(f"Retrieved stats for match {match.external_id}")
        except ClientResponseError:
          print(f"Could not get match stats for {match.external_id}")
          next
        
        try:
          response = await client.skill.get_match_skill(match_id=match.external_id, xuids=[self.xbox_user.xuid])
          parsed = await response.parse()
          skill = parsed.value[0].result.rank_recap

          match.pre_match_csr = skill.pre_match_csr.value
          match.post_match_csr = skill.post_match_csr.value
          await match.asave()
        except ClientResponseError:
          print(f"Could not get match skill for {match.external_id}")
          next
        
        match.stats_retrieved = True
        await match.asave()


        
