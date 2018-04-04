from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django.http import Http404

from django.http import HttpResponse
from announcements.models import *

from django.shortcuts import redirect

from django.utils import timezone

from django.template import loader

from .forms import SubmitAnnounceForm

# Register your models here.
from .models import Individual
from .models import Organization
from .models import Affiliation
from .models import Announcement
from .models import Tags
from .models import AnnounceTags
from .models import SubmitTag
from .models import UserSearch
from .models import TagSearch
from .models import Save

@login_required
def detail(request, announcement_id):
	announcement = get_object_or_404(Announcement,pk=announcement_id)
	if ("approve" in request.POST):
		if (~announcement.is_approved()):
			announcement.approve_status = True
			announcement.save()
	elif ("deny" in request.POST):
		if (announcement.is_approved()):
			announcement.approve_status = False
			announcement.save()
	elif ("delete" in request.POST):
		announcement.delete()
		return redirect('/announcements/')
	context = {
		'announcement': announcement,
	}
	return render(request, 'announcements/detail.html', context)

@login_required
def index(request):
	latest_announcement_list = Announcement.objects.all()
	context = {
	'latest_announcement_list': latest_announcement_list,
	}
	return render(request,'announcements/index.html',context)

@login_required
def submit(request):
	if request.method == "POST":
		form = SubmitAnnounceForm(request.POST)
		if form.is_valid():
			new_announce = form.save(commit=False)
			new_announce.submit_date = timezone.now()
			new_announce.approve_status = False
			new_announce.submitter = request.user.username
			new_announce.save()
			return redirect('/announcements/')
	else:
		form = SubmitAnnounceForm()
	return render(request, 'announcements/submit.html', {'form':form})
