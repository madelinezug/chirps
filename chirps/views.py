from django.http import HttpResponse
from django.shortcuts import render

from chirps.models import .

def atext(request, announcement_id):
    try
        text = Announcement.announce_text
        context = {'announcement_id': announcement_id}
    except Announcement.DoesNotExist:
        raise Http404("Announcement does not exist")
    return render(request,'chirps/atext.html', context)
