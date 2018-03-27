from django.shortcuts import render

from django.http import HttpResponse
<<<<<<< HEAD
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
=======
from django.template import loader

# Register your models here.
from .models import Individual
from .models import Organization
from .models import Affiliation
from .models import Announcement
from .models import Tags
from .models import AnnounceTags
from .models import SubmitAnnouncement
from .models import SubmitTag
from .models import UserSearch
from .models import TagSearch
from .models import Save

def detail(request, announcement_id):
	return HttpResponse("You're looking announcement %s" %announcement_id)

def index(request):
    latest_announcement_list = Announcement.objects.all()
    template = loader.get_template('announcements/index.html')
    context = {
        'latest_announcement_list': latest_announcement_list,
    }
    return HttpResponse(template.render(context, request))
>>>>>>> f5370922d1ac25c4088152bbf293c654ff15d815
