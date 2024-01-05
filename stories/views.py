# stories/views.py
import os
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StoryForm
from .models import Story
from django.conf import settings
from gtts import gTTS
from django.urls import reverse
from django.http import HttpResponse, FileResponse
from PyPDF2 import PdfReader
import pygame

# Initialize Pygame mixer
pygame.mixer.init()


def play_audio(audio_file_path):
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()


def home(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text']
            pdf_file = form.cleaned_data['pdf_file']

            if pdf_file:
                # Read content from the PDF file
                pdf_content = ""
                pdf_reader = PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    pdf_content += pdf_reader.pages[page_num].extract_text()

                # Save the story with timestamp
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                story = Story(text=pdf_content)
                story.save()

                # Create media folder if it doesn't exist
                media_folder = os.path.join(settings.MEDIA_ROOT, 'stories')
                os.makedirs(media_folder, exist_ok=True)

                # Convert text to speech with timestamp using gTTS
                audio_file_path = os.path.join(media_folder, f'story_{timestamp}.mp3')
                tts = gTTS(text=pdf_content, lang='en')
                tts.save(audio_file_path)

                # Play the audio using Pygame
                play_audio(audio_file_path)

                return redirect('home')  # Redirect to clear form after submission

            elif text:
                # The existing text handling logic remains unchanged
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                story = Story(text=text)
                story.save()

                # Create media folder if it doesn't exist
                media_folder = os.path.join(settings.MEDIA_ROOT, 'stories')
                os.makedirs(media_folder, exist_ok=True)

                # Convert text to speech with timestamp using gTTS
                audio_file_path = os.path.join(media_folder, f'story_{timestamp}.mp3')
                tts = gTTS(text=text, lang='en')
                tts.save(audio_file_path)

                # Play the audio using Pygame
                play_audio(audio_file_path)

                return redirect('home')  # Redirect to clear form after submission

    else:
        form = StoryForm()

    audio_files = Story.objects.order_by('-timestamp')

    audio_urls = [{'url': reverse('audio_detail', args=[str(story.id)]), 'timestamp': story.timestamp} for story in
                  audio_files]

    return render(request, 'stories/home.html', {'form': form, 'audio_files': audio_urls})


# Add the audio_detail function
def audio_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    # Ensure consistent timestamp formatting
    timestamp_str = story.timestamp.strftime("%Y%m%d%H%M%S")
    audio_file_path = os.path.join(settings.MEDIA_ROOT, 'stories', f'story_{timestamp_str}.mp3')

    # Check if the file exists before attempting to open it
    if os.path.exists(audio_file_path):
        return FileResponse(open(audio_file_path, 'rb'), content_type='audio/mp3')
    else:
        return HttpResponse("Audio file not found.", status=404)
