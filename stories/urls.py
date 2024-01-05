# stories/urls.py

from django.urls import path
from .views import home, audio_detail


urlpatterns = [
    path('', home, name='home'),
    path('audio/<int:story_id>/', audio_detail, name='audio_detail'),
]
