from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Question, Tag, Answer
from .forms import AnswerCreateForm, QuestionCreateForm

class TagNames:
	'''Названия тэгов'''
	def get_tags(self):
		return Tag.objects.all()

class QuestionView(ListView, TagNames):
	'''Выводит вопросы'''
	model = Question

	def get_queryset(self):
		queryset = Question.objects.all() \
			.annotate(num_likes=Count('likes', distinct=True)) \
			.annotate(num_comments=Count('answers', distinct=True))

		if self.request.GET.getlist('tags'):
			queryset = queryset \
				.filter(tags__slug__in=self.request.GET.getlist('tags'))

		if self.request.GET.get('radio') == 'popularity':
			queryset = queryset.order_by('-num_likes')
		else:
			queryset = queryset.order_by('-timestamp')

		paginator = Paginator(queryset, 10)

		page = self.request.GET.get('page')
		try:
			queryset = paginator.page(page)
		except PageNotAnInteger:
			queryset = paginator.page(1)
		except EmptyPage:
			queryset = paginator.page(paginator.num_pages)

		return queryset.object_list

class QuestionDetailView(DetailView):
	'''Вопрос по айди'''
	model = Question

	def get_queryset(self):
		return Question.objects.all() \
			.annotate(num_likes=Count('likes', distinct=True)) \
			.annotate(num_comments=Count('answers', distinct=True)) \

class CreateQuestionView(TagNames, View):
	'''Создание вопроса'''

	def post(self, request, *args, **kwargs):
		data = request.POST
		if data.get('question', None) and data.get('content', None):
			question = Question.objects.create(
				question=data['question'],
				content=data['content'],
				user=request.user
			)
			for tag in data.getlist('tags', []):
				question.tags.add(get_object_or_404(Tag, slug=tag))
		return redirect(reverse('question-list'))

	def get(self, request, *args, **kwargs):
		return render(request, 'question/question_create.html', context={'tags': Tag.objects.all()})

class CreateAnswerView(View):
	'''Создание ответа'''

	def post(self, request, *args, **kwargs):
		content = request.POST.get('content', None)
		print(request.POST)
		if content:
			ans = Answer.objects.create(
				user=request.user,
				question_id=kwargs['pk'],
				content=content
			)
			print(ans)
		return redirect(reverse('question-detail', kwargs=kwargs))

	# def get(self, request, *args, **kwargs):
		# return redirect(reverse('question-detail', kwargs=kwargs, context={'user': request.user}))


class CreateLike(View):
	'''Создание лайка'''

	@login_required
	def post(self, request, *args, **kwargs):
		user = request.user
		question_id = request.POST.get('question', None)
		like, fl = Like.objects.get_create(
			user=user,
			question_id=question_id
		)
		if fl:
			like.detele()
			return HttpResponse('Лайк удален')
		else:
			return HttpResponse('Лайк добавлен')

class EmptyRouteView(View):
	'''Пустой роут'''
	def get(self, request, *args, **kwargs):
		return redirect(reverse('question-list'))