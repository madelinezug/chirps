from django.db import models

class Individual(models.Model):
    email = models.CharField(max_length=250, primary_key=True)
    password = models.CharField(max_length=50)
    admin_status = models.BooleanField()

class Organization(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description_text = models.CharField(max_length=500)
    admin_user = models.ForeignKey(Individual, on_delete=models.PROTECT)

class Affiliation(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    admin = models.ForeignKey(Individual, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('org','admin'),)

class Announcement(models.Model):
    announce_ID = models.IntegerField(primary_key=True)
    announce_text = models.TextField()
    submit_date = models.DateField()
    expire_date = models.DateField()
    approve_status = models.BooleanField()
    submitter = models.ForeignKey(Individual, related_name = 'submitter', on_delete=models.PROTECT)
    approver = models.ForeignKey(Individual, related_name = 'approver', on_delete=models.PROTECT)

class Tags(models.Model):
    tag_text = models.CharField(max_length=10, primary_key=True)
    approved = models.BooleanField()

class AnnounceTags(models.Model):
    the_announcement = models.ForeignKey(Announcement, on_delete=models.PROTECT)
    the_tag = models.ForeignKey(Tags, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('the_announcement','the_tag'),)

class SubmitAnnouncement(models.Model):
    submit_announce = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(Individual, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('submit_announce','user'),)

class SubmitTag(models.Model):
    tag_submitter = models.ForeignKey(Individual, on_delete=models.PROTECT)
    submitted_tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('tag_submitter','submitted_tag'),)

class UserSearch(models.Model):
    user_searching_user = models.ForeignKey(Individual, related_name = 'searcher', on_delete=models.PROTECT)
    searched_user = models.ForeignKey(Individual, related_name = 'searched', on_delete=models.PROTECT)
    search_time = models.TimeField()
    search_date = models.DateField()

    class Meta:
        unique_together = (('user_searching_user','searched_user'),)

class TagSearch(models.Model):
    user_searching_tag = models.ForeignKey(Individual, on_delete=models.PROTECT)
    searched_tag = models.ForeignKey(Tags, on_delete=models.PROTECT)
    tag_search_time = models.TimeField()
    tag_search_date = models.DateField()

    class Meta:
        unique_together = (('user_searching_tag','searched_tag'),)

class Save(models.Model):
    saver = models.ForeignKey(Individual, on_delete=models.PROTECT)
    saved_announce = models.ForeignKey(Announcement, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('saver','saved_announce'),)
