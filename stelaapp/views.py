from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import CandidateForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Candidate, Profile, Vote_Record

def index(request):
    candidates = Candidate.objects.all()
    return render(request, "stelaapp/index.html", {"candidates": candidates})

@login_required
def candidate_edit(request):
    profile = Profile.objects.get(user = request.user)
    if profile.isCandidate:
        if request.method == 'POST':
            candidate_form = CandidateForm(request.POST, request.FILES)
            if candidate_form.is_valid():
                candidate = candidate_form.save(commit=False)
                candidate.profile = request.user.profile
                candidate.save()
                messages.success(request, ('Your edit was successful!'))
                return redirect('/')
        else:
            try:
                candidate = Candidate.objects.get(profile = profile)
                candidate_form = CandidateForm(instance=candidate)
            except Candidate.DoesNotExist:
                candidate_form = CandidateForm()
        return render(request, "stelaapp/candidate_edit.html", {'candidate_form': candidate_form,})
    else:
        return redirect("/profile/edit")

def candidate_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    candidate = get_object_or_404(Candidate, profile = profile)

    canUserVote = False
    didUserVote = False

    if request.user.is_authenticated:
        # user can only vote for one candidate for the same position
        positionCount = Vote_Record.objects.filter(voter=request.user, position=candidate.position).count()
        if positionCount == 0:
            canUserVote = True

        candidateCount = Vote_Record.objects.filter(voter=request.user, candidate=candidate, position=candidate.position).count()
        if candidateCount != 0:
            didUserVote = True

    return render(request, "stelaapp/view_candidate.html", {"candidate": candidate, "canUserVote": canUserVote, "didUserVote": didUserVote})

@login_required
def vote(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    candidate = get_object_or_404(Candidate, profile = profile)

    count = Vote_Record.objects.filter(voter=request.user, position = candidate.position).count()
    if count == 0:
        vote_record = Vote_Record(voter=request.user, candidate=candidate, position=candidate.position)
        vote_record.save()
        candidate = Candidate.objects.get(profile = candidate.profile)
        candidate.votes += 1
        candidate.save()
    
    return redirect("/{}".format(username))

@login_required
def unvote(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    candidate = get_object_or_404(Candidate, profile = profile)

    count = Vote_Record.objects.filter(voter=request.user, candidate = candidate).delete()[0]
    if count > 0:
        candidate = Candidate.objects.get(profile = candidate.profile)
        candidate.votes -= 1
        candidate.save()

    return redirect("/{}".format(username))