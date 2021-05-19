from django.core.validators import MaxLengthValidator
from django.db import models
from django.conf import settings
from django.utils import timezone

class University(models.Model):
    universityId = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return "Name: {}, Address: {}".format(self.name, self.address)

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

class User(models.Model):
    userId = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    isCandidate = models.BooleanField(default=False)
    studentIdNumber = models.CharField(max_length=11)
    faculty = models.CharField(max_length=200)
    DoB = models.DateTimeField()
    universityId = models.ForeignKey(University,on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} {}".format(self.first_name,self.last_name)

class Candidate(models.Model):
    candidateId = models.IntegerField(primary_key=True)
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    interestsId = models.ForeignKey(Interests,on_delete=models.CASCADE)
    listId = models.ForeignKey(List,on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='cars')
    aboutMe = models.CharField(max_length=500)

    def __str__(self):
        return "{}".format(self.aboutMe)

    



