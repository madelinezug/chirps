from django import forms

from .models import Announcement

class SubmitAnnounceForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ['announce_text','announce_ID','expire_date',]
