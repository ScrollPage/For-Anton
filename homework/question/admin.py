from django.contrib import admin
from .models import Question, Tag, Like, Answer

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Answer)