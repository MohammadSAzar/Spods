from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView


from .models import CustomUserModel, ContentMaker, BusinessOwner
from .forms import RegistrationForm, CMInfoCompletionForm, BOInfoCompletionForm, CMInfoEditForm, BOInfoEditForm
from .checkers import send_otp, get_random_otp, otp_time_checker


# ---------------------------------- Auth ----------------------------------
def registration_view(request):
    form = RegistrationForm
    if request.method == 'POST':
        try:
            if 'phone_number' in request.POST:
                phone_number = request.POST.get('phone_number')
                user = CustomUserModel.objects.get(phone_number=phone_number)
                if user.otp_code is not None and otp_time_checker(user.phone_number):
                    request.session['user_phone_number'] = user.phone_number
                    return HttpResponseRedirect(reverse('verification'))
                otp = get_random_otp()
                send_otp(phone_number, otp)
                user.otp_code = otp
                user.is_active = False
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
    return render(request, 'sponsorships/registration.html', context)


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
            print('IS LOGGED IN')
            return HttpResponseRedirect(reverse('dashboard'))
        context = {
            'phone_number': phone_number,
        }
        return render(request, 'sponsorships/verification.html', context)
    except CustomUserModel.DoesNotExist:
        return HttpResponseRedirect(reverse('registration'))


# -------------------------------- Dashboard --------------------------------
def dashboard_view(request):
    phone_number = request.session.get('user_phone_number')
    if phone_number:
        user = CustomUserModel.objects.get(phone_number=phone_number)
    else:
        user = request.user
    context = {
        'user': user,
        }
    return render(request, 'sponsorships/dashboard.html', context=context)


def dashboard_channel_view(request):
    # User
    context = {}
    phone_number = request.session.get('user_phone_number')
    if phone_number:
        user = CustomUserModel.objects.get(phone_number=phone_number)
    else:
        user = request.user
    context['user'] = user

    # Post
    if request.method == 'POST':
        if user.info_status == 'nc':
            form_cm_comp = CMInfoCompletionForm(request.POST, request.FILES)
            if form_cm_comp.is_valid():
                content_maker = form_cm_comp.save(commit=False)
                content_maker.save()
                user.content_maker = content_maker
                form_cm_comp.save()
                user.info_status = 'ip'
                user.save()
                messages.success(request, "اطلاعات شما دریافت شد، نتیجه فرایند احراز هویت بزودی تعیین می‌شود.")
                return HttpResponseRedirect(reverse('dashboard'))
            context['form_cm_comp'] = form_cm_comp

        if user.info_status == 'bo':
            form_cm_comp = CMInfoCompletionForm(request.POST, request.FILES)
            current_profile = get_object_or_404(BusinessOwner, user=user)
            if form_cm_comp.is_valid():
                content_maker = form_cm_comp.save(commit=False)
                content_maker.email = current_profile.email
                content_maker.save()
                user.content_maker = content_maker
                form_cm_comp.save()
                user.info_status = 'ip'
                user.save()
                messages.success(request, "اطلاعات شما دریافت شد، نتیجه فرایند احراز هویت بزودی تعیین می‌شود.")
                return HttpResponseRedirect(reverse('dashboard'))
            context['form_cm_comp'] = form_cm_comp

        if user.info_status == 'cm' or user.info_status == 'du':
            current_profile = get_object_or_404(ContentMaker, user=user)
            form_cm_edit = CMInfoEditForm(request.POST, request.FILES, instance=current_profile)
            if form_cm_edit.is_valid():
                form_cm_edit.save()
                messages.success(request, "اطلاعات شما با موفقیت اصلاح شد.")
                return HttpResponseRedirect(reverse('dashboard'))
            context['form_cm_edit'] = form_cm_edit

    # Get
    else:
        print('ASS')
        form_cm_comp = CMInfoCompletionForm()
        context['form_cm_comp'] = form_cm_comp
        if user.info_status == 'cm' or user.info_status == 'du':
            current_profile = get_object_or_404(ContentMaker, user=user)
            form_cm_edit = CMInfoEditForm(instance=current_profile)
            context['form_cm_edit'] = form_cm_edit

    return render(request, 'sponsorships/dashboard_channel.html', context=context)


def dashboard_business_view(request):
    # User
    context = {}
    phone_number = request.session.get('user_phone_number')
    if phone_number:
        user = CustomUserModel.objects.get(phone_number=phone_number)
    else:
        user = request.user
    context['user'] = user

    # Post
    if request.method == 'POST':
        if user.info_status == 'nc':
            form_bo_comp = BOInfoCompletionForm(request.POST, request.FILES)
            if form_bo_comp.is_valid():
                business_owner = form_bo_comp.save(commit=False)
                business_owner.save()
                user.business_owner = business_owner
                form_bo_comp.save()
                user.info_status = 'ip'
                user.save()
                messages.success(request, "اطلاعات شما دریافت شد، نتیجه فرایند احراز هویت بزودی تعیین می‌شود.")
                return HttpResponseRedirect(reverse('dashboard'))
            context['form_bo_comp'] = form_bo_comp

        if user.info_status == 'cm':
            form_bo_comp = BOInfoCompletionForm(request.POST, request.FILES)
            current_profile = get_object_or_404(ContentMaker, user=user)
            if form_bo_comp.is_valid():
                business_owner = form_bo_comp.save(commit=False)
                business_owner.email = current_profile.email
                business_owner.save()
                user.business_owner = business_owner
                form_bo_comp.save()
                user.info_status = 'ip'
                user.save()
                messages.success(request, "اطلاعات شما دریافت شد، نتیجه فرایند احراز هویت بزودی تعیین می‌شود.")
                return HttpResponseRedirect(reverse('dashboard'))
            context['form_bo_comp'] = form_bo_comp

        if user.info_status == 'bo' or user.info_status == 'du':
            current_profile = get_object_or_404(BusinessOwner, user=user)
            form_bo_edit = BOInfoEditForm(request.POST, request.FILES, instance=current_profile)
            if form_bo_edit.is_valid():
                form_bo_edit.save()
                messages.success(request, "اطلاعات شما با موفقیت اصلاح شد.")
                return HttpResponseRedirect(reverse('dashboard'))
            context['form_bo_edit'] = form_bo_edit
    # Get
    else:
        print('ASS')
        form_bo_comp = BOInfoCompletionForm()
        context['form_bo_comp'] = form_bo_comp
        if user.info_status == 'bo' or user.info_status == 'du':
            current_profile = get_object_or_404(BusinessOwner, user=user)
            form_bo_edit = BOInfoEditForm(instance=current_profile)
            context['form_bo_edit'] = form_bo_edit

    return render(request, 'sponsorships/dashboard_business.html', context=context)


def dashboard_positions_view(request):
    pass


def dashboard_requests_view(request):
    pass


def dashboard_history_view(request):
    pass


