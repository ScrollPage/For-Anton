from django.views.generic import ListView, DetailView
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.http import HttpResponse

from .models import Question, Tag
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
			.annotate(num_comments=Count('answers', distinct=True)) \
			.filter(tags__slug__in=self.request.GET.getlist('tags'))

		if self.request.GET.get('popularity'):
			return queryset.order_by('-num_likes')
		else:
			return queryset.order_by('-timestamp')

class QuestionDetailView(DetailView):
	'''Вопрос по айди'''
	model = Question

class CreateQuestionView(View):
	'''Создание вопроса'''

	@login_required
	def post(self, request, *args, **kwargs):
		form = QuestionCreateForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			form.user = self.request.user
			form.save()
		return redirect(reverse('question-list'))

class CreateAnswerView(View):
	'''Создание ответа'''

	@login_required
	def post(self, request, *args, **kwargs):
		form = AnswerCreateForm(request.POST)
		if form.is_valid():
			form.save(commit=False)
			form.question_id = kwargs['pk']
			form.user = request.user
			form.save()
		return redirect(reverse('question-detail', kwargs=kwargs))

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