from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.templatetags.static import static

class University(models.Model):
    universityid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.name)

class Interests(models.Model):
    interestId = models.IntegerField(primary_key=True)
    interest = models.CharField(max_length=100)

    def __str__(self):
        return "Interest: {}".format(self.interest)

class List(models.Model):
    listId = models.IntegerField(primary_key=True)
    listName= models.CharField(max_length=200)
    
    def __str__(self):
        return "List name: {}".format(self.listName)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isCandidate = models.BooleanField(default=False)
    studentIdNumber = models.CharField(max_length=11)
    faculty = models.CharField(max_length=200)
    DoB = models.DateField(null=True,blank=True)
    university = models.ForeignKey(University,on_delete=models.CASCADE,db_column='university', null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.studentIdNumber)

class Candidate_Position(models.Model):
    candidate_position_id = models.IntegerField(primary_key=True)
    name = name = models.CharField(max_length=100)

    def __str__(self):
        return "{}".format(self.name)

class Candidate(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    interestsId = models.ForeignKey(Interests,on_delete=models.CASCADE, null=True)
    listId = models.ForeignKey(List,on_delete=models.CASCADE, null=True)
    photo = models.ImageField(null=True, blank=True)
    aboutMe = models.CharField(max_length=500)
    solutions = models.CharField(max_length=500)
    position = models.ForeignKey(Candidate_Position,on_delete=models.CASCADE)
    votes = models.IntegerField(null=True, default=0)
    photo = models.ImageField(null=True, blank=True)

    def get_photo(self):
        if self.photo:
            return self.photo.url
        return static("images/default_photo.png")

class Vote_Record(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.ForeignKey(Candidate_Position,on_delete=models.CASCADE)
    
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=Profile)
def decandidate(sender, instance , created , **kwargs):
    if created:
        return
    #previous = Profile.objects.get(id=instance.id)
    if instance.isCandidate == False:
        Candidate.objects.filter(profile = instance.id).delete()
        Vote_Record.objects.filter(candidate = instance.id).delete()
    return

# @receiver(post_save, sender=Candidate)
# def revert_photo_to_default_after_delete(sender, instance , created , **kwargs):
#     if created:
#         return
#     #previous = Profile.objects.get(id=instance.id)
#     if not instance.photo:
#         Candidate.objects.filter(profile = instance.id).delete()
#         Vote_Record.objects.filter(candidate = instance.id).delete()
#     return
