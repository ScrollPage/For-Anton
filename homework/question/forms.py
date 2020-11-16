from django import forms

from .models import Answer, Question, Tag

class AnswerCreateForm(forms.ModelForm):
	'''Форма ответа'''

	class Meta:
		model = Answer
		fields = ['content']

class QuestionCreateForm(forms.ModelForm):
	'''Форма вопроса'''

	class Meta:
		model = Question
		fields = ['question', 'content', 'tags']

	def __init__(self, *args, **kwargs):
		super(QuestionCreateForm, self).__init__(*args, **kwargs)
		self.fields['tags'].widget = forms.widgets.CheckboxSelectMultiple()
		self.fields['tags'].help_text = ''
		self.fields['tags'].queryset = Tag.objects.all()