from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django.http import Http404

from django.contrib.auth.models import User

from django.http import HttpResponse

from django.shortcuts import redirect

from django.utils import timezone

from django.template import loader

# include forms
from .forms import SubmitAnnounceForm
from .forms import UserForm

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

def sign_up(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			new_individual = form.save(commit=False)
			new_individual.admin_status = False
			new_individual.save()
			user = User.objects.create_user(request.POST['username'],request.POST['email'],
				request.POST['password'])
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			user.save()
			return redirect('/accounts/login')
	else:
		form = UserForm()
	return render(request,'announcements/sign_up.html',{'form':form})


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
