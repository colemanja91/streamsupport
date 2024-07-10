from django.shortcuts import render

from django.db.models import Avg, Max, Sum
from haloinfinite.models import Match, PlaylistAsset, UserPlaylistCSR, XBoxUser

RANK_ICON_BASE_URL = "https://trackercdn.com/cdn/tracker.gg/halo-infinite/skills/c/"

def ranked_slayer(request, gamertag):
  user = XBoxUser.objects.filter(gamertag=gamertag).first()
  slayer_playlist = PlaylistAsset.objects.current_ranked_slayer()
  csr = UserPlaylistCSR.objects.filter(xbox_user=user, playlist_asset=slayer_playlist).first()

  rank = f"{csr.tier} {csr.sub_tier}"
  rank_icon_url = f"{RANK_ICON_BASE_URL}{csr.tier.lower()}-{csr.sub_tier}.png"

  matches = Match.objects.not_ended_early().ranked_slayer().filter(xbox_user=user)
  kills = matches.aggregate(Sum('kills'))['kills__sum']
  deaths = matches.aggregate(Sum('deaths'))['deaths__sum']
  assists = matches.aggregate(Sum('assists'))['assists__sum']
  kda = round((kills + (assists/3))/deaths, 2)

  context = {
    'rank': rank,
    'rank_icon_url': rank_icon_url,
    'matches': matches.count(),
    'wins': matches.aggregate(Sum('rounds_won'))['rounds_won__sum'],
    'kda': kda,
    'accuracy': round(matches.aggregate(Avg('accuracy'))['accuracy__avg'], 2),
    'max_spree': matches.aggregate(Max('max_killing_spree'))['max_killing_spree__max']
  }

  return render(request, 'ranked_slayer_overlay.html', context)
