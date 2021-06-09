from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField
from stelaapp.models import Profile
from stelaapp.models import University
from django.forms.widgets import DateInput

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','first_name', 'last_name', 'password1','password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        labels = {
        'studentIdNumber': ('Student ID Number'),
        'DoB': ('Date of Birth'),
        'university':('University'),
        'isCandidate': ('I am a candidate.'),
        }
        widgets = {
            'DoB': DateInput(attrs={'type': 'date'}), 
        }
        fields = ('studentIdNumber','university', 'faculty','isCandidate','DoB')
        
class UploadPeselForm(forms.Form):
    id_photo = forms.ImageField()

    labels = {
       'id_photo': ('Upload a photo of your student ID card'),
    }
    fields = ('id_photo',)