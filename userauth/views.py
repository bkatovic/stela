from django.shortcuts import render, redirect
from .forms import UserForm
from .forms import ProfileForm
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

@transaction.atomic
def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            profile_form = ProfileForm(request.POST, instance=user.profile)  # Reload the profile form with the profile instance
            profile_form.full_clean()
            profile_form.save() 
            messages.success(request, ('Your profile was successfully created!'))
            login(request, user)
            if profile_form.cleaned_data['isCandidate']:
                return redirect('/candidate/edit')
            else:
                return redirect('/')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, "register.html", {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
@transaction.atomic
def edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            if form.cleaned_data['isCandidate']:
                return redirect('/candidate/edit')
            else:
                return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit.html', {
        'form': form
    })