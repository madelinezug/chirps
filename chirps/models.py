from django.db import models

class Individual(models.Model):
    email = models.CharField(max_length=250, primary_key=True)
    password = models.CharField(max_length=50)
    admin_status = models.BooleanField()

class Organization(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description_text = models.CharField(max_length=500)
    admin_user = models.ForeignKey(Individual)

class Affiliation(models.Model):
    org = models.ForeignKey(Organization)
    admin = models.ForeignKey(Individual)

    class Meta:
        unique_together = (('org','admin'),)

class Announcement(models.Model):
    announce_ID = models.IntegerField(primary_key=True)
    announce_text = models.TextField()
    submit_date = models.DateField()
    expire_date = models.DateField()
    approve_status = models.BooleanField()
    submitter = models.ForeignKey(Individual)
    approver = models.ForeignKey(Individual)

class Tags(models.Model):
    tag_text = models.CharField(max_length=10, primary_key=True)
    approved = models.BooleanField()

class AnnounceTags(models.Model):
    the_announcement = models.ForeignKey(Announcement)
    the_tag = models.ForeignKey(Tags)

    class Meta:
        unique_together(('the_announcment','the_tag'),)

class SubmitAnnouncement(models.Model):
    submit_announce = models.ForeignKey(Announcement)
    user = models.ForeignKey(Individual)

    class Meta:
        unique_together(('submit_announce','user'),)

class SubmitTag(models.Model):
    tag_submitter = models.ForeignKey(Individual)
    submitted_tag = models.ForeignKey(Tags)

    class Meta:
        unique_together(('tag_submitter','submitted_tag'),)

class UserSearch(models.Model):
    user_searching_user = models.ForeignKey(Individual)
    searched_user = models.ForeignKey(Individual)
    search_time = models.TimeField()
    search_date = models.DateField()

    class Meta:
        unique_together(('searching_user','searched_user'),)

class TagSearch(models.Model):
    tag_searching_user = models.ForeignKey(Individual)
    searched_tag = models.ForeignKey(Tags)
    tag_search_time = models.TimeField()
    tag_search_date = models.DateField()

    class Meta:
        unique_together(('tag_search_user','searched_tag'),)

class Save(models.Model):
    saver = models.ForeignKey(Individual)
    saved_announce = models.ForeignKey(Announcement)

    class Meta:
        unique_together(('saver','saved_announce'),)
        
