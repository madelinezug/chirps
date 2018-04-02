from django.shortcuts import get_object_or_404, render
from django.http import Http404

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from announcements.models import *

from django.template import loader

from .forms import SubmitAnnounceForm

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
	announcement = get_object_or_404(Announcement,pk=announcement_id)
	return render(request,"announcements/detail.html",{'announcement': announcement})

def index(request):
    latest_announcement_list = Announcement.objects.all()
    context = {
        'latest_announcement_list': latest_announcement_list,
    }
    return render(request,'announcements/index.html',context)




def submit(request):
   if request.method == "POST":
      form = SubmitAnnounceForm(request.POST)
      if form.is_valid():
        new_announce = form.save(commit=False)
      new_announce.save()
      return redirect('/')
   else:
       form = SubmitAnnounceForm()
   return render(request, 'announcements/submit.html', {'form': form})
