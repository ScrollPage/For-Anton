from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth import logout, authenticate, login
from django.urls import reverse

from .forms import LoginForm, RegistrationForm

class LoginView(View):
	'''Вход в систему'''

	def post(self, request, *args, **kwargs): 
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(
				request,
				email=cd['email'],
				password=cd['password']
			)
			if user is None:
				return redirect(reverse('login'))

			if not user.is_active:
				return redirect(reverse('login'))

			login(request, user)
			return redirect(reverse('question-list'))
		return render(request, 'accounts/login.html')

	def get(self, request, *args, **kwargs):
		return render(request, 'accounts/login.html')

class LogoutView(View):
	'''Выход из системы'''

	def get(self, request, *args, **kwargs):
		logout(request)
		return redirect(reverse('question-list'))

class RegisterView(View):
	'''Регистрация'''
	def get(self, request, *args, **kwargs):
		return render(request, 'accounts/register.html')

	def post(self, request, *args, **kwargs):
		form = RegistrationForm(request.POST)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.set_password(form.cleaned_data["password"])
			new_user.save()

			return redirect(reverse('question-list'))

		return render(request, "accounts/register.html")