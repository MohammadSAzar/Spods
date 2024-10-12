from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView


from .models import CustomUserModel
from .forms import RegistrationForm
from .checkers import send_otp, get_random_otp, otp_time_checker


# ---------------------------------- Auth ----------------------------------
def registration_cm_view(request):
    form = RegistrationForm
    if request.method == 'POST':
        try:
            if 'phone_number' in request.POST:
                phone_number = request.POST.get('phone_number')
                user = CustomUserModel.objects.get(phone_number=phone_number)
                user.type = 'cm'
                if user.otp_code is not None and otp_time_checker(user.phone_number):
                    request.session['user_phone_number'] = user.phone_number
                    return HttpResponseRedirect(reverse('verification'))
                otp = get_random_otp()
                send_otp(phone_number, otp)
                user.otp_code = otp
                user.save()
                request.session['user_phone_number'] = user.phone_number
                return HttpResponseRedirect(reverse('verification'))
        except CustomUserModel.DoesNotExist:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                otp = get_random_otp()
                send_otp(phone_number, otp)
                user.otp_code = otp
                user.is_active = False
                user.save()
                request.session['user_phone_number'] = user.phone_number
                return HttpResponseRedirect(reverse('verification'))
    context = {
        'form': form,
    }
    return render(request, 'sponsorships/registration_cm.html', context)


def registration_bo_view(request):
    form = RegistrationForm
    if request.method == 'POST':
        try:
            if 'phone_number' in request.POST:
                phone_number = request.POST.get('phone_number')
                user = CustomUserModel.objects.get(phone_number=phone_number)
                user.type = 'bo'
                if user.otp_code is not None and otp_time_checker(user.phone_number):
                    request.session['user_phone_number'] = user.phone_number
                    return HttpResponseRedirect(reverse('verification'))
                otp = get_random_otp()
                send_otp(phone_number, otp)
                user.otp_code = otp
                user.save()
                request.session['user_phone_number'] = user.phone_number
                return HttpResponseRedirect(reverse('verification'))
        except CustomUserModel.DoesNotExist:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                otp = get_random_otp()
                send_otp(phone_number, otp)
                user.otp_code = otp
                user.is_active = False
                user.save()
                request.session['user_phone_number'] = user.phone_number
                return HttpResponseRedirect(reverse('verification'))
    context = {
        'form': form,
    }
    return render(request, 'sponsorships/registration_bo.html', context)


def verification_view(request):
    try:
        phone_number = request.session.get('user_phone_number')
        user = CustomUserModel.objects.get(phone_number=phone_number)
        if request.method == 'POST':
            if not otp_time_checker(user.phone_number) or user.otp_code != int(request.POST.get('otp')):
                return HttpResponseRedirect(reverse('verification'))
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        context = {
            'phone_number': phone_number,
        }
        return render(request, 'sponsorships/verification.html', context)
    except CustomUserModel.DoesNotExist:
        return HttpResponseRedirect(reverse('registration'))


