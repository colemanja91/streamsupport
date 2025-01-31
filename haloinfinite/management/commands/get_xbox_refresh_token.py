from django.core.management.base import BaseCommand, CommandError
from haloinfinite.models import XBoxUser
from haloinfinite.services import SpnkrService

import asyncio

class Command(BaseCommand):
  help = "Start flow to set a refresh token for the given user"

  def add_arguments(self, parser):
      parser.add_argument("xbox_user_id", type=int)

  def handle(self, *args, **options):
    xbox_user_id = options["xbox_user_id"]
    try:
      xbox_user = XBoxUser.objects.get(pk=xbox_user_id)
    except XBoxUser.DoesNotExist:
      raise CommandError(f"XBoxUser {xbox_user_id} does not exist")
    
    spnkr = SpnkrService(xbox_user)
    asyncio.run(spnkr.get_refresh_token())
