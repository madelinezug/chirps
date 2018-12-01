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

from django.db.models import Q

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.password_validation import ValidationError

import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey

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
			admin_stat = False#len(request.POST.getlist('admin')) > 0
			email = request.POST['email']
			if not (email.endswith('pomona.edu')):
				no_match = "Please enter a valid Pomona College email."
			elif User.objects.filter(email=email):
				no_match = "This email is already in use. Please try again."
			else:
				backend = default_backend()
				salt = os.urandom(16)
				key_gen = PBKDF2HMAC(
					algorithm=hashes.SHA256(),
					length=32,
					salt=salt,
					iterations=100000,
					backend=backend
				)
				byte_pass = bytes(request.POST['password'], encoding='utf-8')
				hash_pass = key_gen.derive(byte_pass)

				new_individual = Individual(email=email,password =request.POST['password'],chirp_pass=hash_pass,chirp_salt=salt,first=request.POST['first'],last=request.POST['last'],admin_status=admin_stat)
				user = User.objects.create_user(email, email,
					request.POST['password'])
				user.first_name = request.POST['first']
				user.last_name = request.POST['last']
				user.admin_status = admin_stat

				password = request.POST['password']
				try:
					validation_result = validate_password(password, user=user, password_validators=None)
					new_individual.save()
					user.save()
					return redirect('/accounts/login')
				except ValidationError as e:
					no_match = ''.join(e)
		else:
			no_match = "Passwords did not match. Please try again."

	return render(request,'announcements/sign_up.html',{ 'no_match': no_match})


@login_required
def detail(request, announcement_id):
	try:
		announcement = get_object_or_404(Announcement,pk=announcement_id)
	except:
		return render(request,'announcements/error.html',{'error':"No announcement with this ID number"})
	try:
		user = get_object_or_404(Individual,pk=request.user.username)
	except:
		return redirect('/accounts/login')

	# get the announcement tags
	announce_tags = AnnounceTags.objects.filter(the_announcement=announcement)
	num_tags = len(announce_tags)

	if Save.objects.filter(saver=user,saved_announce=announcement).exists():
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
				to_email = [announcement.submitter.email]
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
	elif ("delete" in request.POST):
		if(announcement.submitter==user or user.admin_status):
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
		'announce_tags':announce_tags,
		'num_tags':num_tags,
		'already_saved':already_saved,
		'user':user,
	}
	return render(request, 'announcements/detail.html', context)

@login_required
def index(request):
	approved_chirps_list = Announcement.objects.filter(approve_status=True, expire_date__gte=timezone.now()).order_by('-submit_date')

	try:
		user = get_object_or_404(Individual,pk=request.user.username)
	except:
		return redirect('/accounts/login')

	if request.method == "POST":
		search_key = request.POST["search_key"]
		return redirect('/announcements/search/' + search_key)

	if approved_chirps_list:
		#paginator
		paginator = Paginator(approved_chirps_list, 10)
		page = request.GET.get('page')
		approved_chirps_list = paginator.get_page(page)

	context = {
		'approved_chirps_list': approved_chirps_list,
		'user':user,
	}
	return render(request,'announcements/index.html',context)

@login_required
def email_digest(request):
	approved_chirps_list = Announcement.objects.filter(approve_status=True, expire_date__gte=timezone.now()).order_by('-submit_date')
	try:
		user = get_object_or_404(Individual,pk=request.user.username)
	except:
		return redirect('/accounts/login')

	context = {
		'approved_chirps_list': approved_chirps_list,
		'user':user,
	}

	subject = "Here's your Chirps email digest!"
	from_email = settings.EMAIL_HOST_USER
	recievers = []
	to_email = []
	for user in User.objects.all():
		to_email.append(user.email)

	with open(settings.BASE_DIR + "/announcements/templates/emails/email_digest.txt") as f:
		signup_message = f.read()
		message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
		html_template = get_template("emails/email_digest.html").render(context)
		message.attach_alternative(html_template, "text/html")
		message.send()



	return render(request,'announcements/email_digest.html',context)

@login_required
def submit(request):
	try:
		all_tags = get_object_or_404(Tags,approved=True)
	except:
		all_tags = []

	if Individual.objects.filter(pk=request.user.username).exists():
		current_user = Individual.objects.get(pk=request.user.username)
	else:
		return redirect('/accounts/login')

	if request.method == "POST":
		if "search" in request.POST:
			search_key = request.POST["search_key"]
			return redirect('/announcements/search/' + search_key)
		else:
			new_announce = Announcement(announce_text=request.POST["announce_text"],announce_title=request.POST["announce_title"], announce_img=request.POST["announce_img"],
			submit_date=timezone.now(),expire_date=request.POST["expire_date"],approve_status=Individual.objects.get(pk=request.user.username).admin_status,submitter=Individual.objects.get(pk=request.user.username))
			new_announce.save()

			# save the tag and associate it with the announcement
			submit_tag_list = request.POST['tag_text'].split(",")
			for tag in submit_tag_list:
				if len(tag) > 0 and len(tag) < 40:
					tag = tag.strip()
					tag = tag.lower()
					if not Tags.objects.filter(pk=tag).exists():
						new_tag = Tags(tag_text=tag,approved=Individual.objects.get(pk=request.user.username).admin_status)
						new_tag.save()
					if not AnnounceTags.objects.filter(the_announcement=new_announce,the_tag=Tags.objects.get(pk=tag)).exists():
						announce_tag_pair = AnnounceTags(the_announcement=new_announce,the_tag=Tags.objects.get(pk=tag))
						announce_tag_pair.save()

			if(current_user.admin_status):
				new_announce.approve_status = True
				new_announce.save()
				tags_for_this_announce = new_announce.get_tags()
				for tag_assoc in tags_for_this_announce:
					tag = tag_assoc.the_tag
					if not tag.approved:
						tag.approved = True
						tag.save()
			else:
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
	return render(request, 'announcements/submit.html', {'all_tags':all_tags,'user':current_user})

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
	if (Save.objects.filter(saver=user, saved_announce__expire_date__gte=timezone.now()).exists()):
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
def pending(request):
	if request.method == "POST":
		search_key = request.POST["search_key"]
		return redirect('/announcements/search/' + search_key)

	try:
		user = get_object_or_404(Individual,pk=request.user.username)
	except:
		return redirect('/acccounts/login')
	pending_announcements_list = None
	if (Announcement.objects.filter(approve_status=False, expire_date__gte=timezone.now()).exists()):
		pending_announcements_list = Announcement.objects.filter(approve_status=False, expire_date__gte=timezone.now()).order_by('-submit_date')

		paginator = Paginator(pending_announcements_list, 10)
		page = request.GET.get('page')
		pending_announcements_list = paginator.get_page(page)

	context = {
		'pending_announcements_list': pending_announcements_list,
		'user': user
	}
	return render(request, 'announcements/pending.html', context)

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

	if (Announcement.objects.filter(submitter=user, expire_date__gte=timezone.now()).exists()):
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

	try:
		user = get_object_or_404(Individual,pk=request.user.username)
	except:
		return redirect('/acccounts/login')

	no_match = ""
	matching_announces = []
	search_key = search_key.strip()
	search_key = search_key.lower()

	is_person = Individual.objects.filter(Q(first=search_key) | Q(last=search_key)).exists()

	if is_person:
		people = Individual.objects.filter(Q(first=search_key) | Q(last=search_key))
	else:
		people = None

	# both user and tags match input
	if (Tags.objects.filter(pk=search_key, approved=True).exists() and is_person):
		# first add people
		if (len(list(people)) >= 1):
			for person in people:
				if (Announcement.objects.filter(submitter=person, approve_status=True, expire_date__gte=timezone.now()).exists()):
					matching_announces.extend(Announcement.objects.filter(submitter=person, approve_status=True, expire_date__gte=timezone.now()).order_by('-submit_date'))

	    # add matching tags
		tag = Tags.objects.get(pk=search_key, approved= True)
		if (AnnounceTags.objects.filter(the_tag=search_key, the_announcement__approve_status=True, the_announcement__expire_date__gte=timezone.now()).exists()):
			matching_announce_assocs = list(AnnounceTags.objects.filter(the_tag=search_key, the_announcement__approve_status=True, the_announcement__expire_date__gte=timezone.now()).order_by('-the_announcement__submit_date'))
			for object in matching_announce_assocs:
				if (object.the_announcement not in matching_announces):
					matching_announces.append(object.the_announcement)
		#sort by date
		matching_announces.sort(key=lambda x: x.submit_date, reverse=True)

	# only tags exist for matching input
	elif (Tags.objects.filter(pk=search_key, approved=True).exists()):
		tag = Tags.objects.get(pk=search_key, approved= True)
		if (AnnounceTags.objects.filter(the_tag=search_key, the_announcement__approve_status=True, the_announcement__expire_date__gte=timezone.now()).exists()):
			matching_announce_assocs = list(AnnounceTags.objects.filter(the_tag=search_key, the_announcement__approve_status=True, the_announcement__expire_date__gte=timezone.now()).order_by('-the_announcement__submit_date'))
			for object in matching_announce_assocs:
				matching_announces.append(object.the_announcement)
			if len(matching_announces) == 0:
				no_match = "No Chirps are currently active with this tag"
		else:
			no_match = "No Chirps are currently active with this tag"

	# only users exist for matching input
	elif (is_person):
		if (len(list(people)) >= 1):
			for person in people:
				if (Announcement.objects.filter(submitter=person, approve_status=True, expire_date__gte=timezone.now()).exists()):
					matching_announces.extend(Announcement.objects.filter(submitter=person, approve_status=True, expire_date__gte=timezone.now()).order_by('-submit_date'))
				matching_announces.sort(key=lambda x: x.submit_date, reverse=True)
				if len(matching_announces) == 0:
					no_match = "No active chirps found by users of this name"
	else:
		no_match = "No tags or individuals match your search"

	paginator = Paginator(matching_announces, 10)
	page = request.GET.get('page')
	matching_announces = paginator.get_page(page)

	context = {
		'no_match': no_match,
		'matching_announces':matching_announces,
		'user':user,
	}
	return render(request, 'announcements/search.html',context)

def edit(request, announcement_id):
	try:
		announcement = get_object_or_404(Announcement,pk=announcement_id)
	except:
		return render(request,'announcements/error.html',{'error':"No announcement with this ID number"})
	title = announcement.announce_title
	text = announcement.announce_text
	assoc_tags = AnnounceTags.objects.filter(the_announcement=announcement)
	old_tags=[]
	for assoc in assoc_tags:
		old_tags.append(str(assoc.the_tag))


	# get old inputs
	month = str(announcement.expire_date.month)
	if len(month) == 1:
		month = "0" + month
	day = str(announcement.expire_date.day)
	if len(day) == 1:
		day = "0" + day
	year = str(announcement.expire_date.year)
	expire = year + "-" + month + "-" + day
	image = announcement.announce_img
	tag_list = ""
	for tag in old_tags:
		tag_list = tag_list + tag + ", "
	tag_list = tag_list[:-2]

	try:
		all_tags = get_object_or_404(Tags,approved=True)
	except:
		all_tags = []

	if Individual.objects.filter(pk=request.user.username).exists():
		current_user = Individual.objects.get(pk=request.user.username)
	else:
		return redirect('/accounts/login')

	if request.method == "POST":
		if "search" in request.POST:
			search_key = request.POST["search_key"]
			return redirect('/announcements/search/' + search_key)
		else:
			# update the announcement
			announcement.announce_text = request.POST["announce_text"]
			announcement.announce_title = request.POST["announce_title"]
			announcement.announce_img = request.POST["announce_img"]
			announcement.expire_date=request.POST["expire_date"]
			announcement.save()

			# save the tag and associate it with the announcement
			submit_tag_list = request.POST['tag_text'].split(",")
			new_tags = []
			remove_tags = old_tags
			print("submitted tags:")
			for tag in submit_tag_list:
				if len(tag) > 0 and len(tag) < 40:
					tag = tag.strip()
					tag = tag.lower()
					new_tags.append(tag)
					print(str(tag))
					# if len(old_tags) > 0:
					# 	if tag in old_tags:
					# 		print("removed " + str(tag))
					# 		remove_tags.remove(tag)
					if not Tags.objects.filter(pk=tag).exists():
						new_tag = Tags(tag_text=tag,approved=Individual.objects.get(pk=request.user.username).admin_status)
						new_tag.save()
					if not AnnounceTags.objects.filter(the_announcement=announcement,the_tag=Tags.objects.get(pk=tag)).exists():
						announce_tag_pair = AnnounceTags(the_announcement=announcement,the_tag=Tags.objects.get(pk=tag))
						announce_tag_pair.save()

			remove_tags = set(old_tags).difference(set(new_tags))
			print("old tags:")
			for tag in old_tags:
				print(str(tag))
			print("remove tags:")
			for tag in remove_tags:
				print(str(tag))

			for tag in remove_tags:
				if AnnounceTags.objects.filter(the_announcement=announcement,the_tag=Tags.objects.get(pk=tag)).exists():
					old_assoc = AnnounceTags.objects.get(the_announcement=announcement,the_tag=Tags.objects.get(pk=tag))
					old_assoc.delete()


			return redirect('/announcements/')
	context = {
		'title': title,
		'text': text,
		'tag_list': tag_list,
		'expire': expire,
		'image': image,
		'all_tags':all_tags,
		'user':current_user
	}
	return render(request,'announcements/edit.html',context)
