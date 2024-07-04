from django.core.management.base import BaseCommand, CommandError
from haloinfinite.models import Match, XBoxUser
from haloinfinite.services import SpnkrService

import asyncio

class Command(BaseCommand):
  help = "Retrieve a user's match stats"

  def add_arguments(self, parser):
      parser.add_argument("xbox_user_id", type=int)

  def handle(self, *args, **options):
    xbox_user_id = options["xbox_user_id"]
    try:
      xbox_user = XBoxUser.objects.get(pk=xbox_user_id)
    except XBoxUser.DoesNotExist:
      raise CommandError(f"XBoxUser {xbox_user_id} does not exist")
    
    matches = Match.objects.filter(stats_retrieved=False)
    print(f"Retrieving stats for {len(matches)} matches")
    
    spnkr = SpnkrService(xbox_user)
    asyncio.run(spnkr.refresh_match_stats(matches))
