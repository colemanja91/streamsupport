from django.views.generic import ListView
from haloinfinite.models import Match

class MatchListView(ListView):
    model = Match
    template_name = 'matches.html'
