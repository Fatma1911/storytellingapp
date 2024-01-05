# stories/models.py
from django.db import models
from django.urls import reverse


class Story(models.Model):
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Story {self.timestamp}'

    def get_absolute_url(self):
        return reverse('audio_detail', kwargs={'story_id': self.timestamp.strftime('%Y%m%d%H%M%S').mp3})
