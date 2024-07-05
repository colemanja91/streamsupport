import asyncio

from .spnkr_service import SpnkrService

class RefreshServiceRecord:
  def __init__(self, xbox_user):
    self.xbox_user = xbox_user
    self.spnkr = SpnkrService(self.xbox_user)
  
  def run(self):
    response = asyncio.run(self.spnkr.refresh_service_record())

    self.xbox_user.servicerecord.wins = response.wins
    self.xbox_user.servicerecord.losses = response.losses
    self.xbox_user.servicerecord.ties = response.ties
    self.xbox_user.servicerecord.matches_completed = response.matches_completed
    self.xbox_user.servicerecord.time_played = response.time_played
    self.xbox_user.servicerecord.save()