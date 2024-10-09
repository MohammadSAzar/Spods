from django import forms
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField

from . import models


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

