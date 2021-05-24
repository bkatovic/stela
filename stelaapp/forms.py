from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import ModelChoiceField
from stelaapp.models import Candidate
from stelaapp.models import University
from django.forms.widgets import DateInput

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        labels = {
        'aboutMe': ('Tell us a little about yourself'),
        'solutions': ("How will you solve students' problems?"),
        'position': ("What position are you candidating for?"),
        }
        fields = ('aboutMe','solutions', 'position')
    