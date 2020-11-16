from django.db import models
from django.urls import reverse

from account.models import Account

class Tag(models.Model):
	'''Тэг'''
	slug = models.SlugField('Слаг', default='')

	def __str__(self):
		return f'{self.slug}'

	class Meta:
		verbose_name = 'Тэг'
		verbose_name_plural = 'Тэги'

class Question(models.Model):
	'''Модель вопроса'''
	user = models.ForeignKey(Account, verbose_name='Пользователь', on_delete=models.CASCADE)
	content = models.TextField('Суть вопроса')
	question = models.CharField('Вопрос', max_length=100)
	tags = models.ManyToManyField(Tag, verbose_name='Тэги')
	timestamp = models.DateTimeField('Время', auto_now_add=True)

	def __str__(self):
		return f'Вопрос пользовател {self.user}'

	def get_absolute_url(self):
		return reverse('question-detail', kwargs={'pk': self.pk})

	class Meta:
		verbose_name = 'Вопрос'
		verbose_name_plural = 'Вопросы'

class Answer(models.Model):
	'''Ответ'''
	question = models.ForeignKey(Question, verbose_name='Лайк к вопросу', on_delete=models.CASCADE, related_name='answers')
	user = models.ForeignKey(Account, verbose_name='Пользователь', on_delete=models.CASCADE)
	content = models.TextField('Ответ')

	def __str__(self):
		return f'Ответ пользователя {self.user} на {self.question}'

	class Meta:
		verbose_name = 'Ответ'
		verbose_name_plural = 'Ответы'

class Like(models.Model):
	'''Лайк'''
	question = models.ForeignKey(Question, verbose_name='Лайк к вопросу', on_delete=models.CASCADE, related_name='likes')
	user = models.ForeignKey(Account, verbose_name='Пользователь', on_delete=models.CASCADE)

	class Meta:
		verbose_name = 'Лайк'
		verbose_name_plural = 'Лайки'