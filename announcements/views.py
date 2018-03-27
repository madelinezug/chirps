from django.shortcuts import render

from django.http import HttpResponse
from announcements.models import .

def index(request):
    return HttpResponse("Hello, world. You're at the announcements index.")



def atext(request, announcement_id):
    try
        text = Announcement.announce_text
        context = {'announcement_id': announcement_id}
    except Announcement.DoesNotExist:
        raise Http404("Announcement does not exist")
    return render(request,'chirps/atext.html', context)
