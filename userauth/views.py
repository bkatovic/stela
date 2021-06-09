from django.shortcuts import render, redirect
from .forms import UserForm
from .forms import UploadPeselForm
from .forms import ProfileForm
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .image_processing.card import detect_card, search_pesel
from stelaapp.models import Profile

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

@login_required
def upload_pesel(request):
    if request.method == 'POST':
        if "upload-form" in request.POST:
            print("helllllo")
            form = UploadPeselForm(request.POST, request.FILES)
            if form.is_valid():
                photo = request.FILES['id_photo']
                card = detect_card(photo)
                pesel = search_pesel(card)
                request.pesel = pesel
                if pesel != None and len(pesel) == 11:
                    return render(request, 'confirm_pesel.html', {
                        'pesel': pesel
                    })
                else:
                    error_msg = "PESEL was not recognized! Please try again." 
                    return render(request, 'upload_pesel.html', {'form': form, 'error_msg': error_msg}) 
        elif "confirm-yes" in request.POST:
                profile = Profile.objects.get(user = request.user)
                profile.pesel = request.POST.get("pesel")
                profile.save()
                messages.success(request, ('Your PESEL was successfully verified!'))
                return redirect("/")
        elif "confirm-no" in request.POST:
            form = UploadPeselForm()
            return render(request, 'upload_pesel.html', {'form': form})
    else:
        form = UploadPeselForm()
        return render(request, 'upload_pesel.html', {'form': form})