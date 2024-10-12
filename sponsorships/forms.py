from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField

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
		fields = ('phone_number', 'otp_code', 'info_status', 'type', 'is_active', 'is_staff', 'is_superuser')

	def clean_password(self):
		return self.initial["password"]


# ---------------------------------- Auth ----------------------------------
class RegistrationForm(forms.ModelForm):
	class Meta:
		model = models.CustomUserModel
		fields = ['phone_number', 'otp_code', 'type']

	def clean(self):
		cleaned_data = super().clean()
		phone_number = cleaned_data.get('phone_number')
		otp_code = cleaned_data.get('otp_code')

		if phone_number and not checkers.phone_checker(phone_number):
			self.add_error('phone_number', 'شماره تلفن همراه وارد شده معتبر نیست.')
		if otp_code and not checkers.otp_checker(otp_code):
			self.add_error('otp_code', 'کد وارد شده معتبر نیست.')

		return cleaned_data

