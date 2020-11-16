from django.urls import path

from .views import (
	QuestionView, 
	QuestionDetailView, 
	CreateAnswerView,
	CreateLike, 
	CreateQuestionView
)

urlpatterns = [
	path('', QuestionView.as_view(), name='question-list'),
	path('<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
	path('answer/create/<int:pk>/', CreateAnswerView.as_view(), name='create-answer'),
	path('like/create/', CreateLike.as_view(), name='create-like'),
	path('create/', CreateQuestionView.as_view(), name='create-question')
]