from django import forms

from .models import Account

class LoginForm(forms.Form):
	email = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.ModelForm):
	'''Форма регистрации'''
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ("username", "email", 'password', 'password2')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd["password"] != cd["password2"]:
			raise forms.ValidationError("Пароли не совпадают")
		else:
			return cd["password2"]