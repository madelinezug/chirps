from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, render
from django.http import Http404

from django.contrib.auth.models import User

from django.http import HttpResponse

from django.shortcuts import redirect

from django.utils import timezone

from django.template.loader import get_template

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template

from django.conf import settings

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# include forms
from .forms import SubmitAnnounceForm
from .forms import SaveAnnounceForm

# Register your models here.
from .models import Individual
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
		if (request.POST['password'] == request.POST['redo_password']):
			admin_stat = len(request.POST.getlist('admin')) > 0
			new_individual = Individual(email=request.POST['email'],password =request.POST['password'],first=request.POST['first'],last=request.POST['last'],admin_status=admin_stat)
			new_individual.save()
			user = User.objects.create_user(request.POST['email'],request.POST['email'],
				request.POST['password'])
			user.first_name = request.POST['first']
			user.last_name = request.POST['last']
			user.admin_status = admin_stat
			user.save()
			return redirect('/accounts/login')
		else:
			no_match = "Passwords did not match. Please try again."

	return render(request,'announcements/sign_up.html',{ 'no_match': no_match})


@login_required
def detail(request, announcement_id):
	try:
		announcement = get_object_or_404(Announcement,pk=announcement_id)
	except:
		return render(request,'error.html',{'error':"No announcement with this ID number"})
	try:
		user = get_object_or_404(Individual,pk=request.user.username)
	except:
		return redirect('/accounts/login')
	form = SaveAnnounceForm(request.POST)
	saved_announcement = ""
	save_announcements_list = Save.objects.all()
	announce_tags = AnnounceTags.objects.filter(the_announcement=announcement)
	num_tags = len(announce_tags)

	if Save.objects.filter(saver=user).exists():
		already_saved = True
	else:
		already_saved = False

	if ("approve" in request.POST):
		if(user.admin_status):
			if (~announcement.is_approved()):
				announcement.approve_status = True
				announcement.save()
				subject = "Your chirp was approved!"
				from_email = settings.EMAIL_HOST_USER
				to_email = [current_user.email]
				with open(settings.BASE_DIR + "/announcements/templates/emails/approved_chirp_email.txt") as f:
					signup_message = f.read()
				message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
				html_template = get_template("emails/approved_chirp_email.html").render()
				message.attach_alternative(html_template, "text/html")
				message.send()
			tags_for_this_announce = announcement.get_tags()
			for tag_assoc in tags_for_this_announce:
				tag = tag_assoc.the_tag
				if not tag.approved:
					tag.approved = True
					tag.save()
			tag.approved = True
			tag.save()
	elif ("deny" in request.POST):
		if(user.admin_status):
			if (announcement.is_approved()):
				announcement.approve_status = False
				announcement.save()
	elif ("delete" in request.POST):
		if(announcement.submitter==user):
			# remove saved instances
			if (Save.objects.filter(saved_announce = announcement).exists()):
				save_delete_list = Save.objects.filter(saved_announce = announcement)
				for saved in save_delete_list :
					saved.delete()
			# remove tag associations
			if (AnnounceTags.objects.filter(the_announcement = announcement).exists()):
				assoc_delete_list = AnnounceTags.objects.filter(the_announcement = announcement)
				for assoc in assoc_delete_list :
					assoc.delete()
			# remove announcement
			announcement.delete()
			return redirect('/announcements/')
	elif (("save" in request.POST) and (request.method == "POST")):
		if (Save.objects.filter(saver=user,saved_announce=announcement).exists()):
			return render(request,'announcements/error.html',{'error':"You have already saved this announcement"})
		else:
			save_announce = Save(saver = user, saved_announce = announcement)
			save_announce.save()
			return redirect('/announcements/saved')
	elif ("unsave" in request.POST):
		try:
			prev_save_announce = get_object_or_404(Save,saver=user,saved_announce=announcement)
		except:
			return render(request,'announcements/error.html',{'error':"You have not saved this announcement"})
		prev_save_announce.delete()
		return redirect('/announcements/saved')
	elif ("search" in request.POST):
		search_key = request.POST["search_key"]
		return redirect('/announcements/search/' + search_key)
	context = {
		'announcement': announcement,
		'save_announcements_list': save_announcements_list,
		'announce_tags':announce_tags,
		'num_tags':num_tags,
		'already_saved':already_saved,
	}
	return render(request, 'announcements/detail.html', context)

@login_required
def index(request):
	latest_announcement_list = Announcement.objects.filter(expire_date__gte=timezone.now()).order_by('-submit_date')

	if request.method == "POST":
		search_key = request.POST["search_key"]
		return redirect('/announcements/search/' + search_key)

	#paginator
	paginator = Paginator(latest_announcement_list, 10)
	page = request.GET.get('page')
	latest_announcement_list = paginator.get_page(page)

	context = {
		'latest_announcement_list': latest_announcement_list,
	}
	return render(request,'announcements/index.html',context)

@login_required
def approve_tag(request):
	unapproved_tags = Tags.objects.filter(approved=False)
	num_unapproved = len(unapproved_tags)
	tags_to_approve = None
	if request.method == "POST":
		tags_selected = request.POST.getlist('checks')
		if len(tags_selected) > 0:
			for tag in tags_selected:
				try:
					sel_tag = get_object_or_404(Tags,pk=tag)
				except:
					return render(request,'error.html',{'error':"One of your selected tags does not exist"})
				if "approve" in request.POST:
					sel_tag.approved = True
					sel_tag.save()
				elif "delete" in request.POST:
					# delete associations with chirps using this tag
					if AnnounceTags.objects.filter(the_tag=sel_tag).exists():
						announce_assocs = AnnounceTags.objects.filter(the_tag=sel_tag)
						for assoc in announce_assocs:
							assoc.delete()
					sel_tag.delete()
			return redirect('/announcements/review_tags')
	context = {
		'unapproved_tags': unapproved_tags,
		'num_unapproved': num_unapproved
	}
	return render(request,'announcements/review_tags.html',context)

@login_required
def submit(request):
	try:
		all_tags = get_object_or_404(Tags,approved=True)
	except:
		all_tags = []
	if request.method == "POST":
		if "search" in request.POST:
			search_key = request.POST["search_key"]
			return redirect('/announcements/search/' + search_key)
		else:
		# ann_form = SubmitAnnounceForm(request.POST)
		# if ann_form.is_valid() :
			# save the announcement
			# new_announce = ann_form.save(commit=False)
			# new_announce = Announcement(announce_ID=request.POST["announce_ID"],announce_text=request.POST["announce_text"],announce_title=request.POST["announce_title"],
			new_announce = Announcement(announce_text=request.POST["announce_text"],announce_title=request.POST["announce_title"], announce_img=request.POST["announce_img"],
			submit_date=timezone.now(),expire_date=request.POST["expire_date"],approve_status=False,submitter=Individual.objects.get(pk=request.user.username))
			# new_announce.submit_date = timezone.now()
			# new_announce.approve_status = False
			# new_announce.submitter = Individual.objects.get(pk=request.user.username)
			new_announce.save()

			# save the tag and associate it with the announcement
			current_user = Individual.objects.get(pk=request.user.username)
			submit_tag_list = request.POST['tag_text'].split(",")
			for tag in submit_tag_list:
				if len(tag) > 0:
					tag = tag.strip()
					tag = tag.lower()
					if not Tags.objects.filter(pk=tag).exists():
						new_tag = Tags(tag_text=tag,approved=False)
						new_tag.save()
					announce_tag_pair = AnnounceTags(the_announcement=new_announce,the_tag=Tags.objects.get(pk=tag))
					announce_tag_pair.save()

			subject = "You submitted a chirp!"
			from_email = settings.EMAIL_HOST_USER
			to_email = [current_user.email]
			with open(settings.BASE_DIR + "/announcements/templates/emails/submit_chirp_email.txt") as f:
				signup_message = f.read()
			message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
			html_template = get_template("emails/submit_chirp_email.html").render()
			message.attach_alternative(html_template, "text/html")
			message.send()
			
			return redirect('/announcements/')
		# else:
			# form = SubmitAnnounceForm()
	return render(request, 'announcements/submit.html', {'all_tags':all_tags})

@login_required
def saved(request):
	if request.method == "POST":
		search_key = request.POST["search_key"]
		return redirect('/announcements/search/' + search_key)

	try:
		user = get_object_or_404(Individual,pk=request.user.username)
	except:
		return redirect('/acccounts/login')
	saved_announcements_list = None
	if (Save.objects.filter(saver=user).exists()):
		saved_announcements_list = Save.objects.filter(saver=user, saved_announce__expire_date__gte=timezone.now()).order_by('-saved_announce__submit_date')

		paginator = Paginator(saved_announcements_list, 10)
		page = request.GET.get('page')
		saved_announcements_list = paginator.get_page(page)

	context = {
		'saved_announcements_list': saved_announcements_list,
		'user': user
	}
	return render(request, 'announcements/saved_announcements.html', context)

@login_required
def my_chirps(request):
	if request.method == "POST":
		search_key = request.POST["search_key"]
		return redirect('/announcements/search/' + search_key)

	try:
		user = get_object_or_404(Individual,pk=request.user.username)
	except:
		return redirect('/acccounts/login')
	my_chirps_announcements_list = None

	if (Announcement.objects.filter(submitter=user).exists()):
		my_chirps_announcements_list = Announcement.objects.filter(submitter=user, expire_date__gte=timezone.now()).order_by('-submit_date')

		paginator = Paginator(my_chirps_announcements_list, 10)
		page = request.GET.get('page')
		my_chirps_announcements_list = paginator.get_page(page)

	context = {
		'my_chirps_announcements_list': my_chirps_announcements_list,
		'user': user
	}
	return render(request, 'announcements/my_chirps.html', context)

@login_required
def search(request, search_key):
	if request.method == "POST":
		search_key = request.POST["search_key"]
		return redirect('/announcements/search/' + search_key)

	no_match = ""
	matching_announces = []
	search_key = search_key.strip()
	search_key = search_key.lower()

	is_first = Individual.objects.filter(first=search_key).exists()
	is_last = Individual.objects.filter(last=search_key).exists()

	if is_first:
		person = Individual.objects.get(first=search_key)
	elif is_last:
		person = Individual.objects.get(last=search_key)
	else:
		person = None


	# search for tags that match the input
	if (Tags.objects.filter(pk=search_key).exists()):
		if (AnnounceTags.objects.filter(the_tag=search_key).exists()):
			matching_announce_assocs = list(AnnounceTags.objects.filter(the_tag=search_key).order_by('-the_announcement__submit_date'))
			for object in matching_announce_assocs:
				announce_o_i = object.the_announcement
				if announce_o_i.expired():
					matching_announce_assocs.remove(AnnounceTags.objects.get(the_announcement=announce_o_i))
				else:
					matching_announces.append(announce_o_i)
			if len(matching_announces) == 0:
				no_match = "No Chirps are currently active with this tag"
		else:
			no_match = "No Chirps have used this tag"

	# search for users which match the input
	elif (is_first or is_last):
		if (Announcement.objects.filter(submitter=person).exists()):
			matching_announces = list(Announcement.objects.filter(submitter=person).order_by('-submit_date'))
			for announce_o_i in matching_announces:
				if announce_o_i.expired():
					matching_announces.remove(Announcement.objects.get(pk=announce_o_i.announce_ID))
			if len(matching_announces) == 0:
				no_match = "No Chirps submitted by this user are currently active"
	else:
		no_match = "No tags or individuals match your search"

	paginator = Paginator(matching_announces, 10)
	page = request.GET.get('page')
	matching_announces = paginator.get_page(page)

	context = {
		'no_match': no_match,
		'matching_announces':matching_announces,
	}
	return render(request, 'announcements/search.html',context)
