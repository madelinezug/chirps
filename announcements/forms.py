from django import forms

from .models import Announcement
from .models import Individual

class SubmitAnnounceForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ['announce_text','announce_ID','expire_date',]

class UserForm(forms.ModelForm):

    class Meta:
        model = Individual
        fields = ['email','first_name','last_name']
