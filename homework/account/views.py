from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth import logout
from django.urls import reverse

from .forms import LoginForm

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
				return HttpResponse('Неправильный логин и/или пароль')

			if not user.is_active:
				return HttpResponse('Ваш аккаунт заблокирован') 

			login(request, user)
			return HttpResponse('Добро пожаловать! Успешный вход')
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