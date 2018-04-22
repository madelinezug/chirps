from django import forms

from .models import Announcement
from .models import Individual
from .models import Tags
from .models import Save

class SubmitAnnounceForm(forms.ModelForm):

    class Meta:
        model = Announcement
        fields = ['announce_text','announce_ID','expire_date',]


class SaveAnnounceForm(forms.ModelForm):

    class Meta:
        model = Save
        fields = ['saver','saved_announce']
