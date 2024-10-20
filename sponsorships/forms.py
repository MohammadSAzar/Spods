from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe

from . import models
from . import checkers


# --------------------------------- Admin ---------------------------------
class AdminPanelUserCreateForm(UserCreationForm):
    class Meta:
        model = models.CustomUserModel
        fields = ('phone_number',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AdminPanelUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.CustomUserModel
        fields = ('phone_number', 'otp_code', 'info_status', 'is_active', 'is_staff', 'is_superuser')

    def clean_password(self):
        return self.initial["password"]


# ---------------------------------- Auth ----------------------------------
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = models.CustomUserModel
        fields = ['phone_number', 'otp_code']

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        otp_code = cleaned_data.get('otp_code')

        if phone_number and not checkers.phone_checker(phone_number):
            self.add_error('phone_number', 'شماره تلفن همراه وارد شده معتبر نیست.')
        if otp_code and not checkers.otp_checker(otp_code):
            self.add_error('otp_code', 'کد وارد شده معتبر نیست.')

        return cleaned_data


# -------------------------------- Dashboard --------------------------------
class CustomClearableFileInput(ClearableFileInput):
    template_name = 'sponsorships/custom_file_field.html'


class CMInfoCompletionForm(forms.ModelForm):
    class Meta:
        model = models.ContentMaker
        fields = ['title', 'creator', 'national_code', 'description', 'platform', 'field', 'link1', 'link2', 'link3', 'link4',
                  'id1', 'id2', 'id3', 'id4', 'min_price', 'email', 'cover', 'general_proposal']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['title', 'creator', 'national_code', 'description', 'platform', 'field', 'link1', 'min_price',
                           'email', 'cover', 'general_proposal']
        for field in required_fields:
            self.fields[field].required = True

    def clean(self):
        cleaned_data = super().clean()
        national_code = cleaned_data.get('national_code')
        min_price = cleaned_data.get('min_price')
        email = cleaned_data.get('email')

        if not checkers.national_code_checker(national_code):
            self.add_error('national_code', 'کد ملی وارد شده معتبر نیست.')
        if not checkers.min_price_checker(min_price):
            self.add_error('min_price', 'حداقل مبلغ اسپانسری برای یک اپیزود پادکست، 1 میلیون تومان است.')
        if not checkers.email_checker(email):
            self.add_error('email', 'ایمیل وارد شده معتبر نیست.')

        return cleaned_data


class CMInfoEditForm(forms.ModelForm):
    class Meta:
        model = models.ContentMaker
        fields = ['title', 'description', 'platform', 'field', 'link1', 'link2', 'link3', 'link4',
                  'id1', 'id2', 'id3', 'id4', 'min_price', 'cover', 'general_proposal']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'cover': CustomClearableFileInput(),
            'general_proposal': CustomClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['title', 'description', 'platform', 'field', 'link1', 'min_price', 'cover', 'general_proposal']
        for field in required_fields:
            self.fields[field].required = True

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        if not checkers.min_price_checker(min_price):
            self.add_error('min_price', 'حداقل مبلغ اسپانسری برای یک اپیزود پادکست، 1 میلیون تومان است.')
        return cleaned_data


class BOInfoCompletionForm(forms.ModelForm):
    class Meta:
        model = models.BusinessOwner
        fields = ['title', 'description', 'field', 'link1', 'link2', 'email', 'year', 'sponsor_experience', 'cover', 'general_proposal']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['title', 'description', 'field', 'link1', 'email', 'year', 'sponsor_experience', 'cover', 'general_proposal']
        for field in required_fields:
            self.fields[field].required = True

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not checkers.email_checker(email):
            self.add_error('email', 'ایمیل وارد شده معتبر نیست.')
        return cleaned_data


class BOInfoEditForm(forms.ModelForm):
    class Meta:
        model = models.BusinessOwner
        fields = ['title', 'description', 'field', 'link1', 'link2', 'year', 'sponsor_experience', 'cover', 'general_proposal']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
            'cover': CustomClearableFileInput(),
            'general_proposal': CustomClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True



