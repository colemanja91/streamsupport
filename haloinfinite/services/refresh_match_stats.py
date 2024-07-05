import asyncio
from aiohttp.client_exceptions import ClientResponseError

from haloinfinite.models import Match
from .spnkr_service import SpnkrService

class RefreshMatchStats:
  def __init__(self, xbox_user):
    self.xbox_user = xbox_user
    self.spnkr = SpnkrService(self.xbox_user)
  
  def run(self):
    matches = Match.objects.filter(stats_retrieved=False)
    print(f"Retrieving stats for {len(matches)} matches")

    for match in matches:
      try:
        response = asyncio.run(self.spnkr.get_match_stats(match.external_id))
        self._update_match_core_stats(match, response)
        print(f"Retrieved stats for match {match.external_id}")
      except ClientResponseError:
        print(f"Could not get match stats for {match.external_id}")
        next
      
      try:
        response = asyncio.run(self.spnkr.get_match_skill(match.external_id))
        self._update_match_skill(match, response)
        print(f"Retrieved skill for match {match.external_id}")
      except ClientResponseError:
        print(f"Could not get match skill for {match.external_id}")
        next
  
  def _update_match_core_stats(self, match, response):
    player_stats = [player for player in response.players if (player.player_id == f"xuid({self.xbox_user.xuid})")][0]
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
    match.stats_retrieved = True
    match.save()
  
  def _update_match_skill(self, match, response):
    skill = response.value[0].result.rank_recap

    match.pre_match_csr = skill.pre_match_csr.value
    match.post_match_csr = skill.post_match_csr.value
    match.save()
  
