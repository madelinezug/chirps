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
from .forms import SaveAnnounceForm

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
	no_match = ""
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			if (request.POST['password'] == request.POST['redo_password']):
				new_individual = form.save(commit=False)
				new_individual.email = request.POST['email']
				new_individual.password = request.POST['password']
				new_individual.admin_status = False
				new_individual.save()
				user = User.objects.create_user(request.POST['email'],request.POST['email'],
					request.POST['password'])
				user.first_name = request.POST['first_name']
				user.last_name = request.POST['last_name']
				user.save()
				return redirect('/accounts/login')
			else:
				no_match = "Passwords did not match. Please try again."
	else:
		form = UserForm()
	return render(request,'announcements/sign_up.html',{'form':form, 'no_match': no_match})


@login_required
def detail(request, announcement_id):
	announcement = get_object_or_404(Announcement,pk=announcement_id)
	user = get_object_or_404(Individual,pk=request.user.username)
	form = SaveAnnounceForm(request.POST)
	saved_announcement = "He we are"
	save_announcements_list = Save.objects.all()
	if ("approve" in request.POST):
		if (~announcement.is_approved()):
			announcement.approve_status = True
			announcement.save()
	elif ("deny" in request.POST):
		if (announcement.is_approved()):
			announcement.approve_status = False
			announcement.save()
	elif ("delete" in request.POST):
		if (Save.objects.filter(saved_announce = announcement).exists()):
			save_delete_list = Save.objects.filter(saved_announce = announcement)
			for saved in save_delete_list :
				saved.delete()
		announcement.delete()
		return redirect('/announcements/')
	elif (("save" in request.POST) and (request.method == "POST")):
		if (Save.objects.filter(saver=user,saved_announce=announcement).exists()):
			saved_announcement = "we already saved this"
		else:
			save_announce = Save(saver = user, saved_announce = announcement)
			save_announce.save()
			if (Save.objects.filter(saver=user,saved_announce=announcement).exists()):
				saved_announcement = "it worked!"
	elif ("unsave" in request.POST):
		saved_announcement = "we tried to unsave"
		prev_save_announce = get_object_or_404(Save,saver=user,saved_announce=announcement)
		prev_save_announce.delete()
		if (Save.objects.filter(saver=user,saved_announce=announcement).exists()):
			saved_announcement = "didn't unsave"
		else:
			saved_announcement = "it unsaved!"
	context = {
		'announcement': announcement,
		'save_announcements_list': save_announcements_list,
		'saved_announcement':saved_announcement
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
			new_announce.submitter = Individual.objects.get(pk=request.user.username)
			new_announce.save()
			return redirect('/announcements/')
	else:
		form = SubmitAnnounceForm()
	return render(request, 'announcements/submit.html', {'form':form})

@login_required
def saved(request):
	user = get_object_or_404(Individual,pk=request.user.username)
	saved_announcements_list = None
	if (Save.objects.filter(saver=user).exists()):
		saved_announcements_list = Save.objects.filter(saver=user)
	context = {
		'saved_announcements_list': saved_announcements_list,
		'user': user
	}
	return render(request, 'announcements/saved_announcements.html', context)
