# stories/forms.py

from django import forms
from .models import Story


class StoryForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}), label='Enter your story:')
    pdf_file = forms.FileField(label='Upload PDF file', required=False)  # Add this line

    class Meta:
        model = Story
        fields = ['text', 'pdf_file']
