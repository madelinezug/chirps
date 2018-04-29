from django.db import models
from datetime import date

class Individual(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=50,default='')
    first = models.CharField(max_length=20,default='')
    last = models.CharField(max_length=30,default='')
    admin_status = models.BooleanField()

    def __str__(self):
        return self.email

    def make_admin(self):
        self.admin_status = True

    def is_admin(self):
        return self.admin_status

class Announcement(models.Model):
    announce_ID = models.AutoField(primary_key=True)
    announce_text = models.TextField()
    announce_title = models.CharField(max_length=30)
    announce_img = models.CharField(max_length=200, blank=True, default='')
    submit_date = models.DateField()
    expire_date = models.DateField()
    approve_status = models.BooleanField()
    submitter = models.ForeignKey(Individual, related_name = 'submitter', on_delete=models.PROTECT)
    # approver = models.ForeignKey(Individual, related_name = 'approver', on_delete=models.PROTECT, default='sarahjin97@gmail.com')

    def __str__(self):
        return self.announce_text

    def approve(self):
        self.approve_status = True

    def is_approved(self):
        return self.approve_status

    def expired(self):
        return date.today() > self.expire_date

    def get_tags(self):
        my_tags = list(AnnounceTags.objects.filter(the_announcement=self.announce_ID))
        return my_tags

    def has_tags(self):
        return AnnounceTags.objects.filter(the_announcement=self.announce_ID).exists()

    def num_tags(self):
        return len(list(AnnounceTags.objects.filter(the_announcement=self.announce_ID)))



class Tags(models.Model):
    tag_text = models.CharField(max_length=40, primary_key=True)
    approved = models.BooleanField()

    def __str__(self):
        return self.tag_text

    def approve(self):
        self.approved = True

    def is_approved(self):
        if self.approved:
            return "approved"
        else:
            return "unapproved"

class AnnounceTags(models.Model):
    the_announcement = models.ForeignKey(Announcement, on_delete=models.PROTECT)
    the_tag = models.ForeignKey(Tags, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('the_announcement','the_tag'),)

    def __str__(self):
        return str(self.the_tag)

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

    def __str__(self):
        return self.user_searching_user + ' searched ' + self.searched_user

class TagSearch(models.Model):
    user_searching_tag = models.ForeignKey(Individual, on_delete=models.PROTECT)
    searched_tag = models.ForeignKey(Tags, on_delete=models.PROTECT)
    tag_search_time = models.TimeField()
    tag_search_date = models.DateField()

    class Meta:
        unique_together = (('user_searching_tag','searched_tag'),)

    def __str__(self):
        return self.user_searching_tag + ' searched ' + self.searched_tag

class Save(models.Model):
    saver = models.ForeignKey(Individual, on_delete=models.PROTECT)
    saved_announce = models.ForeignKey(Announcement, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('saver','saved_announce'),)

    def __str__(self):
        return str(self.saver) + ' saved ' + str(self.saved_announce)

    @classmethod
    def create(cls, user, announcement):
        new_save = cls(saver=user,saved_announce=announcement)
        return new_save
