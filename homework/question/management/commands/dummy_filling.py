from django.core.management import BaseCommand

from datetime import datetime, timezone

from account.models import Account
from question.models import Question, Answer, Like, Tag

class Command(BaseCommand):
	help = u"Fills db with instances"

	def handle(self, *args, **options):
		try:
			user = Account.objects.get(email='dummy@dummy.com')
		except:
			user = Account.objects.create_user(
				email='dummy@dummy.com',
				username='dummy',
				password='QWERTYUIOP123'
			)

		for _ in range(150000):
			Question.objects.create(
				user=user,
				content='DUMMY QUESTION',
				question='????'
			)

		q = Question.objects.get(id=1)
		for _ in range(150000):
			Answer.objects.create(
				user=user,
				question=q,
				content='DUMMY QUESTION',
			)

		for _ in range(3*pow(10, 6)):
			Like.objects.create(
				user=user,
				question=q,
			)
		
		for i in range(20000):
			Tag.objects.create(slug=f'tag#{i}')

		password = 'verystrongpass'

		for i in range(20000):
			Account.objects.create_user(
				email=f'email{i}@mail.ru',
				username=f'username{i}',
				password=password
			)


