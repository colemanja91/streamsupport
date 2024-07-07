from django.urls import path

from . import views

urlpatterns = [
    path('overlays/ranked_slayer', views.ranked_slayer, name='ranked_slayer_overlay')
]
